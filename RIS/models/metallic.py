#!/usr/bin/python
import prman

def drawTeapot(ri,x=0,y=0,z=0) :
  ri.TransformBegin()
  ri.Translate(x,y,z)
  ri.Rotate(45,0,1,0)
  ri.Rotate( -90, 1 ,0 ,0)
  ri.Scale( 0.2, 0.2, 0.2) 
  ri.Geometry( "teapot")
  ri.TransformEnd()  



ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" 
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
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
ri.Translate(0,0,5)
ri.Rotate(-20,1,0,0)


# now we start our world
ri.WorldBegin()
#Lighting We need geo to emit light
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", "float exposure"  : [5]})
ri.Translate( -2, 2 , 0)
ri.Sphere( 0.3, -0.3, 0.3, 360)
ri.AttributeEnd()

# first teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float metallic" : [ 0 ]
                        })
drawTeapot(ri,x=-1)

# second teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float metallic" : [ 0.6 ]
                        })
drawTeapot(ri)

# third teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float roughness" : [ 0.5 ],
                        "float metallic" : [ 1.0 ]
                        })
drawTeapot(ri,x=1)
# floor
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.1,0.8,0.1]
                        })
s=2.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
