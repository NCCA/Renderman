#!/usr/bin/env python
import time, random

# import the python renderman library
import prman

from random import uniform as ru

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Curves.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

ri.Display("Curves.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 3)

ri.TransformBegin()
ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [1, 0, 0]})
points = [0, 0, 0, -1, -0.5, 1, 2, 0.5, 1, 1, 0, -1]
width = [0.01, 0.04]
ri.Curves("cubic", [4], "nonperiodic", {ri.P: points, ri.WIDTH: width})

ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": [0, 0, 1]})
points2 = [0, 0, 0, 3, 4, 5, -1, -0.5, 1, 2, 0.5, 1, 1, 0, -1]
ri.Curves("linear", [5], "nonperiodic", {ri.P: points2, ri.CONSTANTWIDTH: [0.075]})


ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
