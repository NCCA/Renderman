#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import getpass
import time, random

# import the python renderman library
import prman
from Obj import *


def Scene(ri):
    ri.AttributeBegin()
    random.seed(25)
    ri.Color([0.27, 0.04, 0.36])
    Orient = 0
    plank = -5.0
    ri.Color([1, 1, 1])
    ri.Surface(
        "SimpleTexture",
        {
            "float Ka": [1.000],
            "float Kd": [0.500],
            "float Ks": [0.500],
            "float roughness": [0.100],
            "color specularcolor": [1.000, 1.000, 1.000],
            "string TextureName": "renderman.tx",
            "float RepeatS": [4.000],
            "float RepeatT": [4.000],
        },
    )
    face = [-2, -1, -2, 2, -1, -2, -2, -1, 2, 2, -1, 2]
    ri.Patch("bilinear", {"P": face})
    ri.AttributeEnd()

    ri.TransformBegin()
    ri.Translate(0, 0.2, 0.2)
    ri.Rotate(-45, 0, 1, 0)
    objFile = "heli1.obj"
    obj = Obj(objFile, 5)
    ri.Scale(0.4, 0.4, 0.4)

    ri.Surface(
        "SimpleTexture",
        {
            "float Ka": [1.000],
            "float Kd": [0.800],
            "float Ks": [0.500],
            "float roughness": [0.100],
            "color specularcolor": [1.000, 1.000, 1.000],
            "string TextureName": "heli1.tx",
            "float RepeatS": [1.000],
            "float RepeatT": [1.000],
        },
    )
    obj.Polygon(ri, 5)
    ri.TransformEnd()


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "ShaderTest.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, "File " + filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " + time.ctime(time.time()))
ri.Declare("Light1", "string")
ri.Declare("Light2", "string")
ri.Declare("Light3", "string")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("ShaderTest.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()


ri.LightSource("pointlight", {ri.HANDLEID: "Light1", "point from": [3, 2, -2], "float intensity": [12]})
ri.LightSource(
    "spotlight", {ri.HANDLEID: "Light2", "point from": [0, 3, 0], "point to": [0, 0, 0], "float intensity": [3]}
)
ri.LightSource("ambientlight", {ri.HANDLEID: "Light3", "float intensity": [0.2]})
ri.Illuminate("Light1", 1)
ri.Illuminate("Light2", 1)
ri.Illuminate("Light3", 1)


ri.Translate(0, 0, 4)
Scene(ri)


ri.WorldEnd()
# and finally end the rib file
ri.End()
