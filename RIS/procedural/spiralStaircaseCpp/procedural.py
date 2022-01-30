#!/usr/bin/python
import prman

# import the python functions
import sys

sys.path.append("../../common")
from Camera import *
from Transformation import *


ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("spiral.rib")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("spiral.exr", "it", "rgba")
ri.Format(1024, 720, 1)

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1]})
ri.PixelVariance(0.02)
ri.ShadingRate(20)


ri.Integrator("PxrPathTracer", "integrator")
# ri.Integrator ("PxrVisualizer" ,"integrator", {"string style" : "shaded"})
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
# Simple translate for our camera
cam = Camera(Vec4(0, 10, 45), Vec4(0, 0, 0), Vec4(0, 1, 0))
cam.place(ri)


# now we start our world
ri.WorldBegin()

# Lighting We need geo to emit light
ri.TransformBegin()
ri.AttributeBegin()

ri.Declare("domeLight", "string")
lightTx = Transformation()
# lightTx.setPosition(0,1,0)
lightTx.setRotation(90, 0, 0)
ri.ConcatTransform(lightTx.getMatrix())

ri.Light("PxrDomeLight", "domeLight", {"float exposure": [0.1], "string lightColorMap": ["../../disney/studio2.tx"]})

ri.AttributeEnd()
ri.TransformEnd()


ri.AttributeBegin()
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [1.0, 0.0, 0.0]})

ri.TransformBegin()

# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral" "1 0.2 0.35 8 5"] [-5 5 -5 5 -35 35]\n'
ri.ArchiveRecord(ri.VERBATIM, program)


ri.TransformEnd()

ri.TransformBegin()
ri.Translate(-6, -1, 0)
ri.Bxdf(
    "PxrDisney",
    "bxdf",
    {
        "color baseColor": [1.0, 1.0, 1.0],
    },
)
# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral" "5 0.5 1.5 8 15"] [-5 5 -5 5 -35 35]\n'
ri.ArchiveRecord(ri.VERBATIM, program)

ri.TransformEnd()

ri.TransformBegin()
ri.Translate(6, -1, 0)
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [0.0, 0.0, 1.0]})
# param width height depth Case Height Rotation Angle
program = 'Procedural "RunProgram" ["spiral" "2 0.3 0.3 8 12"] [-5 5 -5 5 -35 35]\n'
ri.ArchiveRecord(ri.VERBATIM, program)
ri.TransformEnd()

ri.AttributeEnd()

# floor
ri.TransformBegin()
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [1.0, 1.0, 1.0]})
s = 15.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()

# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
