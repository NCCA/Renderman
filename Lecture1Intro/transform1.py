#!/usr/bin/python
# import the python renderman library
import prman

ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "transform1.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("transform1.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE)

# now we start our world
ri.WorldBegin()
# move back 2 in the z so we can see what we are rendering
ri.Translate(0, 0, 2)
ri.Translate(-1, 0, 0)
ri.Sphere(1, -1, 1, 360)
ri.Translate(1, 0, 0)
ri.Sphere(1, -1, 1, 360)
ri.WorldEnd()
# and finally end the rib file
ri.End()
