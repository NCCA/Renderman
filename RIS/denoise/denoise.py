#!/usr/bin/python
import prman

# import the python functions
import sys

sys.path.append("../common")
from functions import drawTeapot


ri = prman.Ri()  # create an instance of the RenderMan interface

# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format

# Beauty...
ri.DisplayChannel("color Ci")
ri.DisplayChannel("float a")
ri.DisplayChannel("color mse", {"string source": "color Ci", "string statistics": "mse"})

# Shading...
ri.DisplayChannel(
    "color albedo",
    {"string source": "color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)"},
)

ri.DisplayChannel(
    "color albedo_var",
    {
        "string source": "color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)",
        "string statistics": "variance",
    },
)


ri.DisplayChannel("color diffuse", {"string source": "color lpe:C(D[DS]*[LO])|O"})
ri.DisplayChannel("color diffuse_mse", {"string source": "color lpe:C(D[DS]*[LO])|O", "string statistics": "mse"})
ri.DisplayChannel("color specular", {"string source": "color lpe:CS[DS]*[LO]"})
ri.DisplayChannel("color specular_mse", {"string source": "color lpe:CS[DS]*[LO]", "string statistics": "mse"})

# Geometry...
ri.DisplayChannel("float z", {"string source": "float z", "string filter": "gaussian"})
ri.DisplayChannel(
    "float z_var", {"string source": "float z", "string filter": "gaussian", "string statistics": "variance"}
)
ri.DisplayChannel("normal normal", {"string source": "normal Nn"})
ri.DisplayChannel("normal normal_var", {"string source": "normal Nn", "string statistics": "variance"})
ri.DisplayChannel("vector forward", {"string source": "vector motionFore"})
ri.DisplayChannel("vector backward", {"string source": "vector motionBack"})

ri.Display(
    "denoise.exr",
    "openexr",
    "Ci,a,mse,albedo,albedo_var,diffuse,diffuse_mse,specular,specular_mse,z,z_var,normal,normal_var,forward,backward",
    {"int asrgba": [1]},
)
# Hider 'raytrace' 'string pixelfiltermode' 'importance' # ...


# ri.Display('simple.exr', 'it', 'rgba')
ri.Format(1024, 720, 1)

# setup the raytrace / integrators
ri.Hider("raytrace", {"int incremental": [1], "string pixelfiltermode": "importance"})
ri.PixelVariance(0.01)

ri.Integrator("PxrPathTracer", "integrator")

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 30})
# Simple translate for our camera
ri.Translate(0, 0, 5)
ri.Rotate(-20, 1, 0, 0)


# now we start our world
ri.WorldBegin()
# Lighting We need geo to emit light
ri.AttributeBegin()
ri.Declare("areaLight", "string")

ri.Light("PxrEnvDayLight", "areaLight", {"int month": [6], "float hour": [8], "float zone": [0], "float exposure": [2]})
ri.Translate(0, 2, 0)
ri.Scale(2, 2, 2)
ri.Bxdf("PxrDisney", "bxdf", {"color emitColor": [1, 1, 1]})

# ri.Geometry("rectlight")
ri.Sphere(50.0, -1, 1, 360)
ri.AttributeEnd()

# first teapot
ri.Bxdf(
    "PxrDisney",
    "bxdf",
    {"color baseColor": [0.8, 0.2, 0.2], "float subsurface": [0], "color subsurfaceColor": [0.1, 0.1, 0.8]},
)
drawTeapot(ri, x=-1)

# second teapot
ri.Bxdf(
    "PxrDisney",
    "bxdf",
    {"color baseColor": [0.8, 0.2, 0.2], "float subsurface": [0.2], "color subsurfaceColor": [0.1, 0.1, 0.8]},
)
drawTeapot(ri)

# third teapot
ri.Bxdf(
    "PxrDisney",
    "bxdf",
    {"color baseColor": [0.8, 0.2, 0.2], "float subsurface": [0.5], "color subsurfaceColor": [0.1, 0.1, 0.8]},
)
drawTeapot(ri, x=1)
# floor
ri.TransformBegin()
ri.Bxdf("PxrDisney", "bxdf", {"color baseColor": [0.1, 0.8, 0.1]})
s = 2.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
