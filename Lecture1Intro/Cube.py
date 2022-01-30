#!/usr/bin/python
# import the python renderman library
import prman


def Cube(width=1.0, height=1.0, depth=1.0):
    w = width / 2.0
    h = height / 2.0
    d = depth / 2.0
    ri.ArchiveRecord(ri.COMMENT, "Cube Generated by Cube Function")
    # rear
    face = [-w, -h, d, -w, h, d, w, -h, d, w, h, d]
    ri.Patch("bilinear", {"P": face})
    # front
    face = [-w, -h, -d, -w, h, -d, w, -h, -d, w, h, -d]
    ri.Patch("bilinear", {"P": face})
    # left
    face = [-w, -h, -d, -w, h, -d, -w, -h, d, -w, h, d]
    ri.Patch("bilinear", {"P": face})
    # right
    face = [w, -h, -d, w, h, -d, w, -h, d, w, h, d]
    ri.Patch("bilinear", {"P": face})
    # bottom
    face = [w, -h, d, w, -h, -d, -w, -h, d, -w, -h, -d]
    ri.Patch("bilinear", {"P": face})
    # top
    face = [w, h, d, w, h, -d, -w, h, d, -w, h, -d]
    ri.Patch("bilinear", {"P": face})
    ri.ArchiveRecord(ri.COMMENT, "--End of Cube Function--")


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Cube.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")  # filename)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Cube.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 5)
ri.TransformBegin()
ri.Translate(-2, 0, 0)
ri.Rotate(25, 0, 1, 0)
Cube()
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(0, 0, 0)
ri.Rotate(25, 1, 1, 0)
ri.Skew(45.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
Cube(0.8, 0.8, 0.8)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(2, 0, 0)
ri.Rotate(-25, 1, 1, 1)
Cube(0.2, 2, 0.2)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
