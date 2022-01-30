#!/usr/bin/python
from __future__ import print_function
import sys, subprocess

sys.path.append("../../common")
import prman, os, Transformation
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
    ri.Begin("__render")
    ri.Option("searchpath", {"string archive": "../assets/:@"})
    ri.Option("searchpath", {"string texture": "../textures/:@"})

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.DisplayChannel("color Ci", {"string source": ["Ci"]})
    ri.DisplayChannel("float a", {"string source": ["a"]})
    ri.DisplayChannel("normal Nn", {"string source": ["Nn"]})
    ri.DisplayChannel("point Po", {"string source": ["Po"]})
    ri.DisplayChannel("point P", {"string source": ["P"]})

    # note passthrough is in single quotes here!
    ri.DisplayChannel(
        "color albedo",
        {
            "string source": [
                "color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)"
            ]
        },
    )
    ri.DisplayChannel("color directDiffuse", {"string source": ["color lpe:C<RD>[<L.>O]"]})
    ri.DisplayChannel("color directSpecular", {"string source": ["color lpe:C<RS>[<L.>O]"]})
    ri.DisplayChannel("color indirectDiffuse", {"string source": ["color lpe:C<RD>[DS]+[<L.>O]"]})
    ri.DisplayChannel("color indirectSpecular", {"string source": ["color lpe:C<RS>[DS]+[<L.>O]"]})
    ri.DisplayChannel("color subsurface", {"string source": ["color lpe:C<TD>[DS]*[<L.>O]"]})
    ri.DisplayChannel("color shadow", {"string source": ["color lpe:holdouts;unoccluded;C[DS]+<L.>"]})
    ri.DisplayChannel("color occluded", {"string source": ["color lpe:holdouts;C[DS]+<L.>"]})
    ri.DisplayChannel("color __Nworld", {"string source": ["__Nworld"]})
    ri.DisplayChannel("color __Pworld", {"string source": ["__Pworld"]})
    ri.DisplayChannel("color __depth", {"string source": ["__depth"]})
    ri.DisplayChannel("color MatteID0", {"string source": ["MatteID0"]})

    ri.Display(
        "HairAOV.exr",
        "openexr",
        "Ci,a,Nn,Po,P,albedo,directDiffuse,indirectDiffuse,indirectSpecular,subsurface,shadow,occluded,__Nworld,__Pworld,__depth,MatteID0",
        {
            "int asrgba": [1],
            "string exrpixeltype": ["half"],
            "string compression": ["zips"],
            "float compressionlevel": [45],
        },
    )

    ri.Format(width, height, 1)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    ri.Integrator(integrator, "integrator", integratorParams)
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
    ri.Declare("domeLight", "string")
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(100, 0, 0, 1)
    ri.Attribute("visibility", {"int indirect": [0], "int transmission": [0], "int camera": [0]})
    ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "Luxo-Jr_4000x2000.tex"})

    ri.AttributeEnd()
    ri.TransformEnd()

    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Attribute("visibility", {"int indirect": [0], "int transmission": [0], "int camera": [1]})
    ri.Declare("Light0", "string")
    tx = Transformation.Transformation()
    tx.setPosition(-0.9, 0.9, 0.5)
    tx.setRotation(90, 60, 35)
    ri.Identity()
    ri.Transform(tx.getMatrix())
    ri.Light("PxrRectLight", "Light0", {"float intensity": 4})

    tx.setPosition(0.9, 0.9, 0.5)
    tx.setRotation(90, 60, -35)
    tx.setScale(0.2, 0.2, 0.2)
    ri.Identity()
    ri.Transform(tx.getMatrix())
    ri.Light("PxrRectLight", "Light0", {"float intensity": 2})

    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################
    # end lighting
    #######################################################################

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "floor"})
    ri.Bxdf("PxrDiffuse", "smooth", {"color diffuseColor": [0.8, 0.8, 0.8]})
    ri.Polygon({ri.P: [-1, -1, 1, 1, -1, 1, 1, -1, -2, -1, -1, -2]})
    ri.AttributeEnd()

    ri.AttributeBegin()
    HairColour = {
        "Blond": [0.921, 0.898, 0.321],
        "Blue": [0.1, 0.1, 0.8],
        "Dark": [0.1, 0.1, 0.1],
        "Red": [1.0, 0.1, 0.1],
        "Green": [0.1, 1.0, 0.1],
    }

    ri.Pattern(
        "PxrMatteID",
        "PxrMatteID1",
        {
            "int enable": [1],
        },
    )

    ri.Attribute("user", {"color MatteID0": [1, 0, 0]})

    ri.Bxdf(
        "PxrMarschnerHair",
        "id",
        {
            "int diffuseModelType": [0],
            "float diffuseGain": [0.3],
            "color diffuseColor": HairColour.get("Green"),
            "float specularGainR": [1.0],
            "float specularGainTRT": [1.0],
            "float specularGainTT": [1.0],
            "float specularGainGLINTS": [1.0],
            "color specularColorR": [0.2, 0.2, 0.2],
            "color specularColorTRT": HairColour.get("Green"),
            "color specularColorTT": [0.2, 0.2, 0.2],
            "float specularConeAngleR": [4.0],
            "float specularConeAngleTRT": [4.0],
            "float specularConeAngleTT": [4.0],
            "float specularOffset": [-3],
            "float specularIor": [1.55],
            "float specularMixFresnel": [1.0],
            "float specularGlintWidth": [10.0],
            "float specularEccentricity": [1.0],
            "float glowGain": [0.0],
            "color glowColor": [1, 1, 1],
            "float specularEnergyCompensation": [0.0],
            "normal eccentricityDirection": [0, 0, 0],
            "color shadowColor": [0.1, 0.1, 0.1],
            "float presence": [1.0],
            "reference int inputAOV": ["PxrMatteID1:resultAOV"],
        },
    )
    ri.Translate(0, -0.2, -1)
    ri.Rotate(90, 0, 1, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.ReadArchive("hair.rib")

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

    cl.ProcessCommandLine("Hair.rib")
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
