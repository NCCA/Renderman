#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
from functions import drawTeapot
from Camera import *

ri = prman.Ri() # create an instance of the RenderMan interface

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

ri.Integrator ("PxrPathTracer" ,"integrator")

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
cam=Camera(Vec4(-2,2.2,3),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)


# now we start our world
ri.WorldBegin()
#######################################################################
#Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
# position light
ri.Translate(0.0,1.5,5)
ri.Rotate(180,1,0,0)
ri.Rotate(30,1,0,0)
# add geometry for debug (off screen here)
ri.Bxdf( "PxrDisney","bxdf", {"color emitColor" : [ 1,1,1] })
ri.Geometry("rectlight")
# enable light
ri.Light( 'PxrRectLight', 'areaLight',{'float exposure' : [4] })
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################


# first teapot
ri.Pattern( "PxrSeExpr" ,"seTexture",{
				"string expression" : [ "sqrt(($u-0.5)*($u-0.5)*4)*voronoi($P*10,2,0.5,0)"]
        })
ri.Bxdf( "PxrDisney","bxdf", { 
			                        	"color baseColor" : [ 0.8 ,0.2 ,0.2 ],
				                        "reference float metallic" : ["seTexture:resultF"]
                        })
drawTeapot(ri,x=-1)

# second teapot
ri.Pattern( "PxrSeExpr" ,"seTexture",{
				"string expression" : [ "sqrt(($u-0.5)*($u-0.5)*4)*voronoi($P*10,2,0.5,0)"]
        })
ri.Bxdf( "PxrDisney","bxdf", { 
			                        	"color baseColor" : [ 0.8 ,0.2 ,0.2 ],
				                        "reference float metallic" : ["seTexture:resultF"]
                        })

drawTeapot(ri)

# third teapot
ri.Color([1,0,0])
ri.Pattern( "PxrSeExpr" ,"seTexture",{
				"string expression" : [ " fbm(vnoise($P*20) + $P*20/4)"
    ]
        })
ri.Pattern( "PxrSeExpr" ,"seTexture2",{
				"string expression" : [ "vnoise($P*20)"
    ]
        })
ri.Bxdf( "PxrDisney","bxdf", { 
                                "reference color baseColor" : ["seTexture:resultRGB"], 
				                        "reference float metallic" : ["seTexture2:resultF"]

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
