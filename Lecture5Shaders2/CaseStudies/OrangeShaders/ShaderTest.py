#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import getpass
import time

# import the python renderman library
import prman


def Scene(ri):
    ri.Rotate(-140, 1, 0, 0)
    ri.TransformBegin()
    ri.Translate(1, 0, 0)
    ri.TransformBegin()
    ri.Rotate(40, 1, 0, 0)
    ri.Surface(
        "orange",
        {
            "float Ka": [1],
            "float Kd": [0.85],
            "float Ks": [1],
            "color specularcolor": [1, 1, 1],
            "float roughness": [0.18],
        },
    )
    ri.Displacement(
        "orangeDisp",
        {
            "float Km": [0.039],
            "float txtscale": [1],
            "float octaves": [4],
            "float omega": [0.35],
            "float lambda": [2],
            "float threshold": [0],
        },
    )
    ri.TransformEnd()
    ri.Sphere(1, -1, 0, 360)

    ri.TransformBegin()
    ri.Rotate(10, 1, 0, 0)
    ri.Surface(
        "slicedOrange",
        {
            "float Ka": [1],
            "float Kd": [0.95],
            "float Ks": [1],
            "float roughness": [0.18],
            "color specularcolor": [1, 1, 1],
        },
    )
    ri.Displacement(
        "dispVoronoi",
        {
            "float Km": [0.002],
            "float roughness": [0.1],
            "float Scale": [0.1],
            "float Freq": [4],
            "float RepeatX": [0.3],
            "float RepeatY": [0.5],
            "float RepeatZ": [0.5],
        },
    )
    ri.TransformEnd()

    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    ri.TransformBegin()
    ri.Translate(-1, 0, 0)
    ri.Rotate(90, 1, 1, 0)
    ri.TransformBegin()
    ri.Rotate(10, 1, 0, 0)
    ri.Surface(
        "orange",
        {
            "float Ka": [1],
            "float Kd": [0.75],
            "float Ks": [0.5],
            "color specularcolor": [1, 1, 1],
            "float roughness": [0.18],
        },
    )
    ri.Displacement(
        "orangeDisp",
        {
            "float Km": [0.039],
            "float txtscale": [12],
            "float octaves": [12],
            "float omega": [0.35],
            "float lambda": [2],
            "float threshold": [0],
        },
    )
    ri.Sphere(1, -1, 1, 360)
    ri.TransformEnd()
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
ri.Format(720, 576, 1)
ri.ShadingRate([0.1])
ri.PixelSamples(8, 8)
ri.PixelFilter(ri.GAUSSIAN, 2.0, 1.0)  # now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.LightSource("pointlight", {ri.HANDLEID: "Light1", "point from": [3, 2, -2], "float intensity": [12]})
ri.LightSource(
    "spotlight", {ri.HANDLEID: "Light2", "point from": [0, 3, 0], "point to": [0, 0, 0], "float intensity": [3]}
)
ri.LightSource("ambientlight", {ri.HANDLEID: "Light3", "float intensity": [0.3]})
ri.Illuminate("Light1", 1)
ri.Illuminate("Light2", 1)
ri.Illuminate("Light3", 1)

ri.Translate(0, 0, 4)
Scene(ri)


ri.WorldEnd()
# and finally end the rib file
ri.End()
