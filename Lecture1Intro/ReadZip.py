#!/usr/bin/python
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface

# simple colour function to set Bxdf
def Colour(colour):
    ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": colour})


ri.Option("rib", {"string asciistyle": "indented"})

filename = "ReadZip.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
ri.Option("searchpath", {"string archive": "./Archive/"})

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("ReadZip.exr", "it", "rgba")
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
ri.ReadArchive("Archive.zip!Archive.rib")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30, 1, 0, 0)
Colour(colours["green"])
ri.Translate(2.2, 0, 0)
ri.Attribute("identifier", {"name": "cube"})
ri.ReadArchive("Archive.zip!cube.rib")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30, 1, 0, 0)
Colour(colours["blue"])
ri.Translate(-2.2, 0, 0)
ri.Attribute("identifier", {"name": "sphere"})
ri.ReadArchive("Archive.zip!sphere.rib")
ri.TransformEnd()
# end our world

ri.WorldEnd()
# and finally end the rib file
ri.End()
