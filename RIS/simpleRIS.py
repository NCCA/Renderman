#!/usr/bin/python
import prman

ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" #"HelloWorld.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("simple.exr", "it", "rgba")
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (0.01)

ri.Integrator ("PxrDefault" , "integrator")
ri.Integrator ("PxrVCM" ,"integrator")
ri.Integrator ("PxrDirectlighting" ,"integrator")
ri.Integrator ("PxrPathTracer" ,"integrator")

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# now we start our world
ri.WorldBegin()
# move back 2 in the z so we can see what we are rendering
ri.ArchiveRecord(ri.COMMENT, 'move our world back 2 in the z so we can see it')

ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", "float exposure"  : [6]})
ri.Translate( 2.4 ,1 ,2)
ri.Sphere( 0.3, -0.3, 0.3, 360)
ri.AttributeEnd()
ri.TransformEnd()




ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float roughness" : [ 0.5 ], 
                        "float clearcoat" : [ 0.2 ], 
                        "float clearcoatGloss" : [1]
                        })
ri.Translate(0,0,4)

ri.TransformBegin()
ri.Translate( 0,-1.0,0)
ri.Rotate(-90,1,0,0)
ri.Rotate(36,0,0,1)
ri.Scale(0.4,0.4,0.4)
ri.Geometry("teapot")
ri.TransformEnd()
# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
