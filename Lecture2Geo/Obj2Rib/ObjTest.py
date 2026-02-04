#!/usr/bin/env rmanpy3
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import prman
import sys

sys.path.append("../../common")
from Obj import *

objFile = "troll.obj"

obj = Obj(objFile)


ri = prman.Ri()  # create an instance of the RenderMan interface

ri.Option("rib", {"string asciistyle": "indented"})

for frame in range(0, 360, 10):

    filename = "Obj2Rib.%03d.rib" % (frame)
    # this is the begining of the rib archive generation we can only
    # make RI calls after this function else we get a core dump
    ri.Begin(filename)
    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("Obj2Rib.%03d.exr" % (frame), "file", "rgba")
    # Specify PAL resolution 1:1 pixel Aspect ratio
    ri.Format(720, 575, 1)
    # now set the projection to perspective
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

    # now we start our world
    ri.WorldBegin()

    ri.Translate(0, 0, 2)
    ri.TransformBegin()

    ri.Translate(-1, 0, 0)
    ri.Rotate(frame, 0, 1, 0)

    obj.Polygon(ri)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Rotate(frame, 0, 1, 0)

    obj.PointsPolygon(ri)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(1, 0, 0)
    ri.Rotate(frame, 0, 1, 0)

    obj.SubDivisionMesh(ri)
    ri.TransformEnd()

    ri.WorldEnd()
    # and finally end the rib file
    ri.End()
