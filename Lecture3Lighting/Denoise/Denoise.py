#!/usr/bin/env rmanpy3
import prman
import os
import sys
import subprocess

sys.path.append("../")
import ProcessCommandLine as cl

# Main rendering routine
def main(
    filename,
    shadingrate=10,
    pixelvar=0.1,
    fov=48.0,
    width=1024,
    height=720,
    integrator="PxrPathTracer",
    integratorParams={},
):
    print("shading rate {} pivel variance {} using {} {}".format(shadingrate, pixelvar, integrator, integratorParams))
    ri = prman.Ri()  # create an instance of the RenderMan interface

    # this is the begining of the rib archive generation we can only
    # make RI calls after this function else we get a core dump
    ri.Begin(filename)
    ri.Option("searchpath", {"string archive": "../assets/:@"})
    ri.Option("searchpath", {"string shader": "../:@"})

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
        "Denoise.exr",
        "openexr",
        "Ci,a,mse,albedo,albedo_var,diffuse,diffuse_mse,specular,specular_mse,z,z_var,normal,normal_var,forward,backward",
        {"int asrgba": [1]},
    )

    ri.Format(width, height, 1)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1], "string pixelfiltermode": "importance"})
    ri.Integrator(integrator, "integrator", integratorParams)
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)

    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})

    ri.Rotate(12, 1, 0, 0)
    ri.Translate(0, 0.75, 2.5)

    # now we start our world
    ri.WorldBegin()
    #######################################################################
    # Lighting  :- Move the light just before the celling to show direction
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("Light0", "string")
    ri.Translate(0, 0.6, 0)
    ri.Rotate(45, 0, 1, 0)
    ri.Rotate(90, 1, 0, 0)
    ri.Scale(0.5, 0.5, 0.5)
    ri.Light("PxrRectLight", "Light0", {"float intensity": 30})
    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################
    # end lighting
    #######################################################################

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "cornell"})
    ri.ReadArchive("cornell.rib")
    ri.AttributeEnd()

    ri.AttributeBegin()

    ri.Attribute("identifier", {"name": "buddha"})
    ri.TransformBegin()
    ri.Translate(-0.5, -1, 0)
    ri.Rotate(180, 0, 1, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.Attribute("visibility", {"int transmission": [1]})
    ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
    ri.Attribute("user", {"string __materialid": ["greenglass"]})

    ri.Bxdf(
        "PxrSurface",
        "greenglass",
        {
            "color refractionColor": [0, 0.9, 0],
            "float diffuseGain": 0,
            "color specularEdgeColor": [0.2, 1, 0.2],
            "float refractionGain": [1.0],
            "float reflectionGain": [1.0],
            "float glassRoughness": [0.01],
            "float glassIor": [1.5],
            "color extinction": [0.0, 0.2, 0.0],
            "string __materialid": ["greenglass"],
        },
    )
    ri.ReadArchive("buddha.zip!buddha.rib")
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "sphere"})
    ri.Pattern("PxrVariable", "du", {"string variable": "du", "string type": "float"})
    ri.Pattern("PxrVariable", "dv", {"string variable": "dv", "string type": "float"})
    ri.Pattern("starBall", "starBall", {"reference float du": ["du:resultR"], "reference float dv": ["dv:resultR"]})
    ri.Attribute("user", {"string __materialid": ["ball"]})

    ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["starBall:Cout"], "string __materialid": ["ball"]})
    ri.TransformBegin()
    ri.Translate(0.3, -0.7, 0.3)
    ri.Rotate(-30, 0, 1, 0)
    ri.Rotate(20, 1, 0, 0)
    ri.Sphere(0.3, -0.3, 0.3, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "teapot"})
    ri.TransformBegin()
    ri.Translate(0, -1, -0.8)
    ri.Rotate(45, 0, 1, 0)
    ri.Rotate(-90, 1, 0, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.Attribute("user", {"string __materialid": ["teapot"]})

    ri.Bxdf(
        "PxrSurface",
        "plastic",
        {
            "color diffuseColor": [0.04, 0.51, 0.1],
            "color clearcoatFaceColor": [0.5, 0.5, 0.5],
            "color clearcoatEdgeColor": [0.25, 0.25, 0.25],
            "string __materialid": ["teapot"],
        },
    )
    ri.Geometry("teapot")
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("user", {"string __materialid": ["metal"]})

    ri.Bxdf(
        "PxrSurface",
        "metal",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "color specularEdgeColor": [1, 1, 1],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [0.1],
            "integer specularModelType": [1],
            "string __materialid": ["metal"],
        },
    )

    ri.Attribute("identifier", {"name": "ncca"})
    ri.TransformBegin()
    ri.Translate(0, 0.3, 0.8)
    ri.ReadArchive("ncca.rib")
    ri.TransformEnd()
    ri.AttributeEnd()

    # end our world
    ri.WorldEnd()
    # and finally end the rib file
    ri.End()


def checkAndCompileShader(shader):
    if (
        os.path.isfile(shader + ".oso") != True
        or os.stat(shader + ".osl").st_mtime - os.stat(shader + ".oso").st_mtime > 0
    ):
        print("compiling shader %s" % (shader))
        try:
            subprocess.check_call(["oslc", shader + ".osl"])
        except subprocess.CalledProcessError:
            sys.exit("shader compilation failed")


if __name__ == "__main__":
    shaderName = "../starBall"
    checkAndCompileShader(shaderName)

    cl.ProcessCommandLine("Denoise.rib")
    main(
        cl.filename,
        cl.args.shadingrate,
        cl.args.pixelvar,
        cl.args.fov,
        cl.args.width,
        cl.args.height,
        cl.integrator,
        cl.integratorParams,
    )
