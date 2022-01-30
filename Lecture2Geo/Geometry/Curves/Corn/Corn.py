#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import time, random

# import the python renderman library
import prman
import sys

sys.path.append("../../../../common/")

from Camera import *
from Vec4 import *

from random import uniform as ru


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
            pappend(0.1)
            pappend(zpos + ru(minus, plus))

            pappend(xpos + ru(minus, plus))
            pappend(0.2)
            pappend(zpos + ru(minus, plus))

            pappend(xpos + ru(minus, plus))
            pappend(0.3 + ru(-0.1, 0.1))
            pappend(zpos + ru(minus, plus))

            wappend(0.006)
            wappend(0.003)
            npappend(4)
            xpos += inc
        zpos += inc


def UpdateField(points, offset, offset1):
    for i in range(0, len(points), 12):
        points[i + 6] += offset
        points[i + 9] += offset1


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

points = []
width = []
npoints = []
dir = 0
dircount = 0
# BuildField(1.5,0.1,0.01,points,width,npoints)
BuildField(2, 0.4, 0.01, points, width, npoints)

offset = 0.0
cam = Camera(Vec4(0.1, 1.2, 1, 1), Vec4(0, 0, 0, 1), Vec4(0, 1, 0, 0))
cam.fov = 40

for frame in range(0, 1):

    filename = "__render"  #'corn.%03d.rib' %(frame)
    print("processing ", frame)
    # this is the begining of the rib archive generation we can only
    # make RI calls after this function else we get a core dump
    ri.Begin(filename)

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("corn.%03d.exr" % (frame), "it", "rgba")
    # Specify PAL resolution 1:1 pixel Aspect ratio
    ri.Format(720, 576, 1)
    # now set the projection to perspective
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})
    ri.Hider("raytrace", {"int incremental": [1], "int maxsamples": [256]})
    ri.Integrator("PxrPathTracer", "handle", {"float clampLuminance": [10]})

    cam.place(ri)

    # now we start our world
    ri.WorldBegin()

    #######################################################################
    # Lighting We need geo to emit light
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("meshLight", "string")
    ri.Light("PxrMeshLight", "meshLight", {"float intensity": 30})
    ri.ShadingRate(1)
    ri.Sides(1)
    ri.Patch("bilinear", {"P": [-0.25, 0.99, -0.25, 0.25, 0.99, -0.25, -0.25, 0.99, 0.25, 0.25, 0.99, 0.25]})
    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################
    # end lighting
    #######################################################################

    ri.TransformBegin()
    print(offset)

    if dir == 0:
        offset += 0.001
        dircount += 1
        UpdateField(points, offset, offset)
        if dircount == 10:
            dir = 1
            dircount = 0
            offset -= 0.0001
            print("BACK")
    else:
        offset -= 0.001
        dircount += 1
        UpdateField(points, -offset, -offset)
        if dircount == 10:
            dir = 0
            dircount = 0
            offset += 0.0001
            print("FORE")

    ri.Bxdf(
        "PxrMarschnerHair",
        "corn",
        {
            "float specularGainTT": [0.66],
            "color specularColorTRT": [1, 1, 1],
            "color specularColorTT": [1, 1, 1],
            "color diffuseColor": [0.519, 0.325, 0.125],
            "int diffuseModelType": [0],
        },
    )

    ri.Curves("cubic", npoints, "nonperiodic", {ri.P: points, ri.WIDTH: width})

    ri.TransformEnd()
    ri.WorldEnd()
    # and finally end the rib file
    ri.End()
