#!/usr/bin/env rmanpy
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "PointPolygon.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("GeneralPolygon.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 2)

ri.TransformBegin()
ri.Rotate(45, 1, 1, 0)

points = [
    -0.5,
    -0.5,
    -0.5,
    0.5,
    -0.5,
    -0.5,
    -0.5,
    0.5,
    -0.5,
    0.5,
    0.5,
    -0.5,
    -0.5,
    -0.5,
    0.5,
    0.5,
    -0.5,
    0.5,
    -0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
]

npolys = [4, 4, 4, 4, 4, 4]
nvertices = [0, 2, 3, 1, 0, 1, 5, 4, 0, 4, 6, 2, 1, 3, 7, 5, 2, 6, 7, 3, 4, 5, 7, 6]

ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": [1, 0, 0]})

ri.PointsPolygons(npolys, nvertices, {ri.P: points})

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
