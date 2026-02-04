#!/usr/bin/python
import prman

# import the python functions
import sys

sys.path.append("../common")
import Obj
from Camera import Camera
from Vec4 import Vec4
from Transformation import *
import random


ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("simple.exr", "it", "rgba")
ri.Format(1024, 720, 1)

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1]})
ri.PixelVariance(0.01)

ri.Integrator("PxrPathTracer", "integrator")
ri.Option("statistics", {"filename": ["stats.txt"]})

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
# Simple translate for our camera
cam = Camera(Vec4(0, 2, -10), Vec4(0, 0, 0), Vec4(0, 1, 0))
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
ri.Translate(0.0, 4.5, 0)
ri.Rotate(90, 1, 0, 0)
ri.Scale(10, 10, 10)
# add geometry for debug (off screen here)
ri.Bxdf("PxrDisney", "bxdf", {"color emitColor": [1, 1, 1]})
ri.Geometry("rectlight")
# enable light
ri.Light("PxrRectLight", "areaLight", {"float exposure": [0.5]})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################


# load mesh
troll = Obj.Obj("../meshes/troll.obj")
offset = 10
x = -offset
y = -offset

while y < offset:
    while x < offset:
        tx = Transformation()

        ri.TransformBegin()
        tx.setPosition(x, 1.0, y)
        tx.setScale(0.7, random.uniform(0.6, 0.8), 0.7)
        tx.setRotation(0, random.uniform(0, 360), 0)
        ri.ConcatTransform(tx.getMatrix())
        baseColor = [random.uniform(0.2, 1.0), random.uniform(0.2, 1.0), random.uniform(0.2, 1.0)]
        ri.Bxdf(
            "PxrDisney",
            "bxdf",
            {
                "color baseColor": baseColor,
                "float roughness": [random.uniform(0.5, 1.0)],
                "float clearcoat": [random.uniform(0.2, 1.0)],
                "float clearcoatGloss": [random.uniform(0.4, 1.0)],
            },
        )

        troll.SubDivisionMesh(ri)
        # ri.Sphere(1.0,-1,1,360)
        # print x,y
        x = x + 0.6
        ri.TransformEnd()
    y = y + 1.0
    x = -10

# floor
ri.TransformBegin()
ri.Bxdf(
    "PxrDisney",
    "bxdf",
    {
        "color baseColor": [1, 1, 1],
        "float roughness": [0.2],
    },
)
s = 12.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
