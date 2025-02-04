#!/usr/bin/env rmanpy
import prman

# import the python functions
import sys
import sys, os.path, subprocess
import argparse

sys.path.append("../common")
from functions import drawTeapot, drawCube
from Camera import *


def drawScene(ri, zpos=0):

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "torus"})
    ri.TransformBegin()
    ri.Translate(-1.5, 0.5, zpos + 0.1)
    ri.Rotate(45, 0, 1, 0)
    ri.Scale(0.2, 0.2, 0.2)
    ri.Torus(1.00, 0.5, 0, 360, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "teapot"})
    ri.TransformBegin()
    ri.Translate(-1, 0, zpos)
    ri.Rotate(-90, 1, 0, 0)
    ri.Scale(0.1, 0.1, 0.1)
    ri.Geometry("teapot")
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "sphere"})
    ri.TransformBegin()
    ri.Translate(0, 0.3, zpos)
    ri.Sphere(0.3, -1, 1, 360)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Attribute("identifier", {"name": "cube"})
    ri.TransformBegin()
    drawCube(ri, x=1.0, y=0.25, z=zpos, ry=45.0, sx=0.5, sy=0.5, sz=0.5)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.TransformBegin()
    ri.Attribute("identifier", {"name": "disk"})
    ri.Translate(1.8, 0.5, zpos)
    ri.Scale(0.4, 0.4, 0.4)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()
    ri.AttributeEnd()


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

    # now we add the display element using the usual elements
    # FILENAME DISPLAY Type Output format
    ri.Display("rgb.exr", "it", "rgba")
    ri.Format(width, height, 1)

    # setup the raytrace / integrators
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    ri.Integrator(integrator, "integrator", integratorParams)
    ri.Option("statistics", {"filename": ["stats.txt"]})
    ri.Option("statistics", {"endofframe": [1]})

    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})

    # Simple translate for our camera
    cam = Camera(Vec4(-1, 1.5, 3), Vec4(0, 0, 0), Vec4(0, 1, 0))
    cam.place(ri)

    # now we start our world
    ri.WorldBegin()

    #######################################################################
    # Lighting We need geo to emit light
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(100, 0, 0, 1)
    ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "Env_StinsonBeach_1350PM_2k.17.tex"})
    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################

    drawScene(ri, 0)
    drawScene(ri, 1)
    drawScene(ri, 2)

    ri.AttributeBegin()
    ri.Pattern("uvshader", "uvshader")
    ri.Bxdf("PxrDiffuse", "uv", {"reference color diffuseColor": ["uvshader:resultRGB"]})
    drawScene(ri, -1)
    ri.AttributeEnd()

    ri.AttributeBegin()
    # floor
    ri.Attribute("identifier", {"name": "floor"})
    ri.TransformBegin()
    s = 5.0
    face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
    ri.Patch("bilinear", {"P": face})

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
    shaderName = "uvshader"
    checkAndCompileShader(shaderName)

    parser = argparse.ArgumentParser(description="Modify render parameters")

    parser.add_argument(
        "--shadingrate",
        "-s",
        nargs="?",
        const=10.0,
        default=10.0,
        type=float,
        help="modify the shading rate default to 10",
    )

    parser.add_argument(
        "--pixelvar", "-p", nargs="?", const=0.1, default=0.1, type=float, help="modify the pixel variance default  0.1"
    )
    parser.add_argument(
        "--fov", "-f", nargs="?", const=48.0, default=48.0, type=float, help="projection fov default 48.0"
    )
    parser.add_argument(
        "--width", "-wd", nargs="?", const=1024, default=1024, type=int, help="width of image default 1024"
    )
    parser.add_argument(
        "--height", "-ht", nargs="?", const=720, default=720, type=int, help="height of image default 720"
    )

    parser.add_argument("--rib", "-r", action="count", help="render to rib not framebuffer")
    parser.add_argument("--default", "-d", action="count", help="use PxrDefault")
    parser.add_argument("--vcm", "-v", action="count", help="use PxrVCM")
    parser.add_argument("--direct", "-t", action="count", help="use PxrDirect")
    parser.add_argument("--wire", "-w", action="count", help="use PxrVisualizer with wireframe shaded")
    parser.add_argument("--normals", "-n", action="count", help="use PxrVisualizer with wireframe and Normals")
    parser.add_argument("--st", "-u", action="count", help="use PxrVisualizer with wireframe and ST")

    args = parser.parse_args()
    if args.rib:
        filename = "rgb.rib"
    else:
        filename = "__render"

    integratorParams = {}
    integrator = "PxrPathTracer"
    if args.default:
        integrator = "PxrDefault"
    if args.vcm:
        integrator = "PxrVCM"
    if args.direct:
        integrator = "PxrDirectLighting"
    if args.wire:
        integrator = "PxrVisualizer"
        integratorParams = {"int wireframe": [1], "string style": ["shaded"]}
    if args.normals:
        integrator = "PxrVisualizer"
        integratorParams = {"int wireframe": [1], "string style": ["normals"]}
    if args.st:
        integrator = "PxrVisualizer"
        integratorParams = {"int wireframe": [1], "string style": ["st"]}

    main(filename, args.shadingrate, args.pixelvar, args.fov, args.width, args.height, integrator, integratorParams)
