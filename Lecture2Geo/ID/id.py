#!/usr/bin/env rmanpy
# import the python renderman library
import prman


def Cube(width=1.0, height=1.0, depth=1.0,id=0):
    w = width / 2.0
    h = height / 2.0
    d = depth / 2.0
    ri.ArchiveRecord(ri.COMMENT, "Cube Generated by Cube Function")
    ri.Attribute("identifier" , {"int id" : [id]})
    ri.Attribute("identifier" , {"int id2" : [id+2]})
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

filename = "id.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")  # filename)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("id.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 25)
ri.Rotate(-15,1,0,0)


id=0
use_noise=0
for z in range(-10,0) :
    for x in range(-10,10) :
        ri.TransformBegin()
        ri.Translate(x, 0, z)
        ri.AttributeBegin()
        if id > 100 :
            use_noise=1
        ri.Pattern("id_shader", "id_shader", {"int use_noise" : [use_noise]})
        ri.Bxdf("PxrConstant","constant",
        {
            "reference color emitColor" : ["id_shader:RGB"],
            "float presence" : [1],
        })
        Cube(0.4, 0.4, 0.4,id)
        id+=1
        ri.AttributeEnd()
        ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
