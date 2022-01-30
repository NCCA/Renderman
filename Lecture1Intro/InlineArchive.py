#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
# import the python renderman library
import prman


# simple colour function to set Bxdf
def Colour(colour):
    ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": colour})


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "InlineArchive.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

ri.ArchiveBegin("Wave")
ri.Rotate(90, 1, 0, 0)
ri.Sphere(0.030303, -0.030303, 0, 360)
ri.Torus(0.0606061, 0.030303, 0, 180, 360)
ri.Torus(0.121212, 0.030303, 180, 360, 360)
ri.Torus(0.181818, 0.030303, 0, 180, 360)
ri.Torus(0.242424, 0.030303, 180, 360, 360)
ri.Torus(0.30303, 0.030303, 0, 180, 360)
ri.Torus(0.363636, 0.030303, 180, 360, 360)
ri.Torus(0.424242, 0.030303, 0, 180, 360)
ri.Torus(0.484848, 0.030303, 180, 360, 360)
ri.Torus(0.545455, 0.030303, 0, 180, 360)
ri.Torus(0.606061, 0.030303, 180, 360, 360)
ri.Torus(0.666667, 0.030303, 0, 180, 360)
ri.Torus(0.727273, 0.030303, 180, 360, 360)
ri.Torus(0.787879, 0.030303, 0, 180, 360)
ri.Torus(0.848485, 0.030303, 180, 360, 360)
ri.ArchiveEnd()


# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("InlineArchive.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})


# now we start our world
colours = {
    "red": [1, 0, 0],
    "white": [1, 1, 1],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
    "black": [0, 0, 0],
    "yellow": [1, 1, 0],
}


# start our world
ri.WorldBegin()
ri.Translate(0, 0, 10)  # move the global view position
ri.TransformBegin()
ri.Rotate(30, 1, 0, 0)
Colour(colours["red"])
ri.Attribute("identifier", {"name": "Wave1"})
ri.ReadArchive("Wave")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30, 1, 0, 0)
Colour(colours["green"])
ri.Translate(2.2, 0, 0)
ri.Attribute("identifier", {"name": "Wave2"})
ri.ReadArchive("Wave")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30, 1, 0, 0)
Colour(colours["blue"])
ri.Translate(-2.2, 0, 0)
ri.Attribute("identifier", {"name": "Wave3"})
ri.ReadArchive("Wave")
ri.TransformEnd()
# end our world

ri.WorldEnd()
# and finally end the rib file
ri.End()
