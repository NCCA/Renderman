#!/usr/bin/python
import prman

# import the python functions
import sys

sys.path.append("../common")
from functions import drawTeapot
from Camera import *
from Transformation import *


ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
for frame in range(0, 360, 10):

    # this is the begining of the rib archive generation we can only
    # make RI calls after this function else we get a core dump
    ri.Begin("__render")

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("roughness%03d.exr" % (frame), "it", "rgba")
    ri.Format(1024, 720, 1)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.PixelVariance(0.01)

    ri.Integrator("PxrPathTracer", "integrator")

    # now set the projection to perspective
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
    # Simple translate for our camera
    cam = Camera(Vec4(-1.6, 1, 3.5), Vec4(0, 0, 0), Vec4(0, 1, 0))
    cam.place(ri)

    # now we start our world
    ri.WorldBegin()

    # Lighting We need geo to emit light
    ri.TransformBegin()
    ri.AttributeBegin()

    ri.Declare("domeLight", "string")
    lightTx = Transformation()
    lightTx.setPosition(0, 1, 0)
    lightTx.setRotation(90, frame, 180)
    lightTx.setScale(1, 1, 1)
    ri.ConcatTransform(lightTx.getMatrix())
    # ri.Bxdf( "PxrDisney","bxdf", { "color emitColor" : [ 1,1,1] })
    # ri.Geometry('envsphere')

    ri.Light("PxrDomeLight", "domeLight", {"float exposure": [1.0], "string lightColorMap": ["studio2.tx"]})

    ri.AttributeEnd()
    ri.TransformEnd()

    # first teapot
    ri.AttributeBegin()
    ri.Bxdf(
        "PxrDisney",
        "bxdf",
        {"color baseColor": [1.0, 1.0, 1.0], "float metallic": [1], "float roughness": [0], "float specular": [0.5]},
    )
    drawTeapot(ri, x=-1, ry=-45)
    ri.AttributeEnd()

    # second teapot
    ri.Bxdf(
        "PxrDisney",
        "bxdf",
        {"color baseColor": [1.0, 1.0, 1.0], "float metallic": [0.5], "float roughness": [0], "float specular": [0.5]},
    )
    drawTeapot(ri, ry=-45)

    # third teapot
    ri.Bxdf(
        "PxrDisney",
        "bxdf",
        {"color baseColor": [1.0, 1.0, 1.0], "float metallic": [0], "float roughness": [0], "float specular": [0.5]},
    )
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
