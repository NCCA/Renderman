#!/usr/bin/python
import prman

# import the python functions
import sys

sys.path.append("../../common")
from functions import drawTeapot
from Camera import *


ri = prman.Ri()  # create an instance of the RenderMan interface

ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("simple.exr", "it", "rgba")
ri.Format(1024, 720, 1)

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1]})
ri.PixelVariance(0.01)

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
ri.Translate(0.0, 1.5, 5)
ri.Rotate(180, 1, 0, 0)
ri.Rotate(30, 1, 0, 0)
# add geometry for debug (off screen here)
ri.Bxdf("PxrDisney", "bxdf", {"color emitColor": [1, 1, 1]})
ri.Geometry("rectlight")
# enable light
ri.Light("PxrRectLight", "areaLight", {"float exposure": [4]})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################


# first teapot
ri.Pattern(
    "PxrMyFractal", "noiseTexture", {"float frequency": [0.1], "float lacunarity": [2.5], "float erosion": [2.1]}
)

ri.Pattern(
    "PxrToFloat3",
    "promote",
    {
        "reference float inputR": ["noiseTexture:resultF"],
        "reference float inputG": ["noiseTexture:resultF"],
        "reference float inputB": ["noiseTexture:resultF"],
    },
)

ri.Pattern(
    "PxrInvert",
    "invert",
    {
        "reference color inputRGB": ["promote:resultRGB"],
        "int invertChannel0": [0],
        "int invertChannel1": [0],
        "int invertChannel2": [1],
    },
)

ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["invert:resultRGB"]})
drawTeapot(ri, x=-1)


ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["invert:resultRGB"]})
drawTeapot(ri)


ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["invert:resultRGB"]})
drawTeapot(ri, x=1)
# floor
ri.TransformBegin()
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [0.1, 0.8, 0.1]})
s = 2.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
