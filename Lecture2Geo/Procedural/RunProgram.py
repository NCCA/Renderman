#!/usr/bin/env rmanpy3
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin

# import the python renderman library
import prman


def Colour(colour):
    ri.Bxdf("PxrDiffuse", "bxdf", {"color diffuseColor": colour})


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "runprogram.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("runprogram.exr", "file", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 60})

ri.Identity()
ri.ConcatTransform([1.0, 0.0, 0.0, 0.0, 0.0, 0.9, -0.4, 0.0, 0.0, 0.4, 0.9, 0.0, -0.0, -0.0, 16.925824, 1.0])

# now we start our world
ri.WorldBegin()


ri.TransformBegin()
Colour([1, 0, 0])
ri.Translate(0, -1, 0)

# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral.py" "1 0.2 0.35 20 5"] [-5 5 -5 5 -35 35]\n'
ri.Attribute("identifier", {"name": "Spiral1"})
ri.ArchiveRecord(ri.VERBATIM, program)

ri.TransformEnd()
ri.TransformBegin()
Colour([1, 1, 1])
ri.Translate(-6, -1, 0)
# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral.py" "5 0.5 1.5 10 15"] [-5 5 -5 5 -35 35]\n'
ri.Attribute("identifier", {"name": "Spiral2"})
ri.ArchiveRecord(ri.VERBATIM, program)

ri.TransformEnd()

ri.TransformBegin()
Colour([1, 0, 1])
ri.Translate(6, -1, 0)
# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral.py" "2 0.3 0.3 10 12"] [-5 5 -5 5 -35 35]\n'
ri.Attribute("identifier", {"name": "Spiral3"})
ri.ArchiveRecord(ri.VERBATIM, program)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
