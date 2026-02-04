#!/usr/bin/env rmanpy3
# import the python renderman library
import prman

ri = prman.Ri()  # create an instance of the RenderMan interface

# simple colour function to set Bxdf
def Colour(colour):
    ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": colour})


# now we start our world
colours = {
    "red": [1, 0, 0],
    "white": [1, 1, 1],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
    "black": [0, 0, 0],
    "yellow": [1, 1, 0],
}

ri.Option("rib", {"string asciistyle": "indented"})

filename = "__render"
ri.Begin(filename)

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("ObjectBegin.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

# start our world
ri.WorldBegin()
# declare a string so we can refer to the Object by name
ri.Declare("Spheres", "string")
# Now we actually create the Object
ObjHandle = ri.ObjectBegin()
print(ObjHandle)
ri.Sphere(1, -1, 1, 360)
ri.Translate(0, 0, 2)
ri.Scale(0.5, 0.5, 0.5)
ri.Sphere(1, -1, 1, 360)
ri.ObjectEnd()


ri.Translate(0, 0, 14)  # move the global view position
ri.Rotate(90, 1, 0, 0)
Colour(colours["red"])
ri.Attribute("identifier", {"name": "Spheres1"})
ri.ObjectInstance(ObjHandle)
Colour(colours["green"])
ri.Translate(3.2, 0, 0)
ri.Attribute("identifier", {"name": "Spheres2"})
ri.ObjectInstance(ObjHandle)
Colour(colours["blue"])
ri.Translate(-6.2, 0, 0)
ri.Attribute("identifier", {"name": "Spheres3"})
ri.ObjectInstance("%s" % (ObjHandle))
ri.ArchiveRecord("ribfile", "ObjectInstance " + ObjHandle)

# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
