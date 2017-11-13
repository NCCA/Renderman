#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
from functions import drawTeapot
from Camera import *


ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("specularTint.exr", "it", "rgba")
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
ri.Translate(0.0,1.5,3)
ri.Rotate(180,1,0,0)
ri.Rotate(-30,1,0,0)
# add geometry for debug (off screen here)
ri.Bxdf( "PxrDisney","bxdf", {"color emitColor" : [ 1,1,1] })
ri.Geometry("rectlight")
# enable light
ri.Light( 'PxrRectLight', 'areaLight',{'float exposure' : [4] })
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
######################################################################## first teapot
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1.0, 0.0, 0.0], 
                        "float specularTint" : [1],
                        })
drawTeapot(ri,x=-1,ry=-45)
ri.AttributeEnd()

# second teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1.0, 0.0, 0.0], 
                        "float specularTint" : [.5],
                        })
drawTeapot(ri,ry=-45)

# third teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1.0, 0.0, 0.0], 
                        "float specularTint" : [0],
                        })
drawTeapot(ri,x=1,ry=-45)
# floor
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1.0,1.0,1.0]
                        })
s=5.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
