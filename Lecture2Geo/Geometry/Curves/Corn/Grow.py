#!/usr/bin/env rmanpy3
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import random

# import the python renderman library
import prman
import sys

sys.path.append("../../../../common")

from Camera import *
from Vec4 import *



def BuildField(wi, depth, inc, points, width, npoints):
    xmin = -wi / 2.0
    xmax = wi / 2.0
    zmin = -depth / 2.0
    zmax = depth / 2.0
    pappend = points.append
    wappend = width.append
    npappend = npoints.append
    random.seed(1)
    ru = random.uniform
    zpos = zmin
    plus = 0.1
    minus = -0.1
    while zpos < zmax:
        xpos = xmin
        while xpos < xmax:
            pappend(xpos + ru(minus, plus))
            pappend(0)
            pappend(zpos + ru(minus, plus))

            pappend(xpos + ru(minus, plus))
            pappend(0.0)
            pappend(zpos + ru(minus, plus))

            pappend(xpos + ru(minus, plus))
            pappend(0.0)
            pappend(zpos + ru(minus, plus))

            pappend(xpos + ru(minus, plus))
            pappend(0.0)  # .3+ru(-0.1,0.1))
            pappend(zpos + ru(minus, plus))

            wappend(0.006)
            wappend(0.003)
            npappend(4)
            xpos += inc
        zpos += inc


def UpdateField(points, scale):
    for i in range(0, len(points), 12):
        points[i + 4] = scale
        points[i + 7] = 2 * scale
        points[i + 10] = 5 * scale


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

points = []
width = []
npoints = []
dir = 0
dircount = 0
BuildField(1.5, 2, 0.1, points, width, npoints)
# BuildField(1,1,0.5,points,width,npoints)

offset = 0.0
cam = Camera(Vec4(0.1, 0.4, 2, 1), Vec4(0, 0, 0, 1), Vec4(0, 1, 0, 0))
cam.fov = 40

for frame in range(0, 100):

    filename = "__render"  # "corn.%03d.rib" %(frame)
    print("processing ", frame)
    # this is the begining of the rib archive generation we can only
    # make RI calls after this function else we get a core dump
    ri.Begin(filename)

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("growcorn.%03d.exr" % (frame), "file", "rgba")
    # Specify PAL resolution 1:1 pixel Aspect ratio
    ri.Format(720, 576, 1)
    # now set the projection to perspective
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

    cam.place(ri)

    # now we start our world
    ri.WorldBegin()

    ri.TransformBegin()
    print(offset)

    offset += 0.001
    ri.Curves("cubic", npoints, "nonperiodic", {ri.P: points, ri.WIDTH: width})
    UpdateField(points, offset)

    ri.TransformEnd()
    ri.WorldEnd()
    # and finally end the rib file
    ri.End()
