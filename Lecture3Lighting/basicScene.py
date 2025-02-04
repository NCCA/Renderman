#!/usr/bin/env rmanpy
import prman
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
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.ShadingRate(shadingrate)
    ri.PixelVariance(pixelvar)
    # ri.Integrator (integrator ,'integrator',integratorParams)
    ri.Option("statistics", {"filename": ["stats.txt"]})
    ri.Option("statistics", {"endofframe": [1]})
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: fov})

    ri.Rotate(12, 1, 0, 0)
    ri.Translate(0, 0.75, 2.5)

    # now we start our world
    ri.WorldBegin()
    #######################################################################
    # Lighting We need geo to emit light
    #######################################################################
    # no lights for this one!
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
    ri.ReadArchive("buddha.zip!buddha.rib")
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.AttributeBegin()
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


if __name__ == "__main__":
    cl.ProcessCommandLine("testScenes.rib")
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
