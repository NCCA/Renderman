#!/usr/bin/env python
import prman, os
import ProcessCommandLine as cl

# Main rendering routine
def main(
    filename,
    shadingrate=10,
    pixelvar=0.1,
    fov=45.0,
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
    ri.Option("searchpath", {"string archive": "./assets/:@"})

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("rgb.exr", "it", "rgba")
    ri.Format(width, height, 1)

    # setup the raytrace / integrators
    ri.Option("bucket", {"string order": ["horizontal"]})

    ri.Hider(
        "raytrace",
        {
            "int incremental": [1],
            "int minsamples": [16],
            "int maxsamples": [256],
        },
    )
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    ri.Integrator(integrator, "integrator", integratorParams)

    ri.Attribute("visibility", {"int transmission": [1], "int indirect": [1]})
    ri.Attribute("trace", {"int maxdiffusedepth": [5], "int maxspeculardepth": [5]})
    ri.Option("statistics", {"filename": ["stats.txt"]})
    ri.Option("statistics", {"endofframe": [1]})
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})

    ri.Rotate(12, 1, 0, 0)
    ri.Translate(0, 0.75, 2.5)

    # now we start our world
    ri.WorldBegin()
    #######################################################################
    # Lighting
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("meshLight", "string")
    ri.Attribute("identifier", {"name": "ncca"})

    ri.Light(
        "PxrMeshLight",
        "id",
        {
            "float intensity": [4.0],
            "float exposure": [1],
            "color lightColor": [0.8, 0.8, 0.8],
            "int enableTemperature": [1],
            "float temperature": [2500],
            "int areaNormalize": [0],
        },
    )

    ri.Bxdf("PxrBlack", "black")
    ri.Translate(0, 0.6, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.ReadArchive("light.rib")

    ri.AttributeEnd()
    ri.TransformEnd()
    ## light base
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "base", {"color diffuseColor": [0.1, 0.1, 0.1]})
    ri.Translate(0, 0.65, 0)
    ri.Scale(0.4, 0.01, 0.4)
    ri.Attribute("visibility", {"int transmission": [0]})
    ri.ReadArchive("lightBase.rib")
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
    ri.Rotate(-180, 0, 1, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.Attribute("visibility", {"int transmission": [1]})
    ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [8]})
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
        },
    )
    ri.ReadArchive("buddha.zip!buddha.rib")
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Pattern("PxrVariable", "du", {"string variable": "du", "string type": "float"})
    ri.Pattern("PxrVariable", "dv", {"string variable": "dv", "string type": "float"})
    ri.Pattern("starBall", "starBall", {"reference float du": ["du:resultR"], "reference float dv": ["dv:resultR"]})

    ri.Bxdf("PxrDisney", "bxdf", {"reference color baseColor": ["starBall:Cout"]})
    ri.Attribute("identifier", {"name": "sphere"})
    ri.TransformBegin()
    ri.Translate(0.3, -0.7, 0.3)
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
    ri.Geometry("teapot")
    ri.TransformEnd()
    ri.AttributeEnd()
    ri.AttributeBegin()
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
    shaderName = "starBall"
    checkAndCompileShader(shaderName)

    cl.ProcessCommandLine("meshlight.rib")
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
