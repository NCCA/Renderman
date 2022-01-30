#!/usr/bin/python
import prman

# import the python functions
import sys, os.path, subprocess

sys.path.append("../../../common")
from functions import drawTeapot
from Camera import *

"""
function to check if shader exists and compile it, we assume that the shader
is .osl and the compiled shader is .oso If the shader source is newer than the
compiled shader we will compile it. It also assumes that oslc is in the path.
"""


def checkAndCompileShader(shader):
    if (
        os.path.isfile(shader + ".oso") != True
        or os.stat(shader + ".osl").st_mtime - os.stat(shader + ".oso").st_mtime > 0
    ):
        print("compiling shader %s" % (shader))
        try:
            subprocess.check_call(["oslc", shader + ".osl"])
        except subprocess.CalledProcessError:
            sys.exit("shader compilation failed")


shaderName = "distance"
checkAndCompileShader(shaderName)
ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("rgb.exr", "it", "rgba")
ri.Format(1024, 720, 1)

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1]})
ri.PixelVariance(0.02)
ri.ShadingRate(20)


ri.Integrator("PxrPathTracer", "integrator")

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
# Simple translate for our camera
cam = Camera(Vec4(-2, 2.2, 3), Vec4(0, 0, 0), Vec4(0, 1, 0))
cam.place(ri)


# now we start our world
ri.WorldBegin()

#######################################################################
# Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("areaLight", "string")
# position light
ri.Translate(0.0, 1.5, 3)
ri.Rotate(180, 1, 0, 0)
ri.Rotate(-30, 1, 0, 0)
# add geometry for debug (off screen here)
ri.Bxdf("PxrDisney", "bxdf", {"color emitColor": [1, 1, 1]})
ri.Geometry("rectlight")
# enable light
ri.Light("PxrRectLight", "areaLight", {"float exposure": [3]})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################

# set the pattern generation to be from our osl band shader
ri.Pattern("distance", shaderName, {"string shader": shaderName, "color Cin": [1.0, 0.2, 0.0]})


# first teapot
ri.AttributeBegin()
# the colour from the shader is driven by noise, metallic by the noise green channel via the noiseToFloat
ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["%s:Cout" % shaderName]})
drawTeapot(ri, x=-1, ry=-45)
ri.AttributeEnd()
ri.Pattern("distance", shaderName, {"color baseColour": [1.0, 0.2, 0.0], "float repeatU": [4], "float repeatV": [2]})
# second teapot
ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["%s:Cout" % shaderName]})
drawTeapot(ri, ry=-45)
ri.Pattern(
    "distance",
    shaderName,
    {"float repeatU": [8], "float repeatV": [8], "color spotColour": [0, 0, 1], "float fuzz": [0.8]},
)
# third teapot
ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["%s:Cout" % shaderName]})
drawTeapot(ri, x=1, ry=-45)
# floor
ri.TransformBegin()
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [1.0, 1.0, 1.0]})
s = 5.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()

# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
