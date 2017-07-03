#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
from functions import drawTeapot
from Camera import *


ri = prman.Ri() # create an instance of the RenderMan interface

filename = '__render' 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('emit.exr', 'it', 'rgba')
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider('raytrace' ,{'int incremental' :[1]})
ri.PixelVariance (0.01)

ri.Integrator ('PxrDefault' , 'integrator')
ri.Integrator ('PxrVCM' ,'integrator')
ri.Integrator ('PxrDirectlighting' ,'integrator')
ri.Integrator ('PxrPathTracer' ,'integrator')

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
cam=Camera(Vec4(-2,2.2,3),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)



# now we start our world
ri.WorldBegin()


# first teapot
ri.AttributeBegin()
ri.Bxdf( 'PxrDisney','bxdf', { 
                        'color baseColor' : [ 0.5, 0.0, 0.0]
                        })
drawTeapot(ri,x=-1,ry=-45)
ri.AttributeEnd()



ri.AttributeBegin()

# second teapot
# name the light
ri.Declare('areaLight' ,'string')
#  A simple Area Light
ri.Light( 'PxrMeshLight', 'areaLight',{                               'float intensity' : [0.5],
'float exposure' : [2.5],
'color lightColor' : [0.8,0.8,0.2] })


drawTeapot(ri,ry=-45,z=1)
ri.AttributeEnd()


# third teapot
ri.Bxdf( 'PxrDisney','bxdf', { 
                        'color baseColor' : [ 1.0, 0.0, 0.0], 
                        })
drawTeapot(ri,x=1,ry=-45)
# floor
ri.TransformBegin()
ri.Bxdf( 'PxrDisney','bxdf', { 
                        'color baseColor' : [ 1.0,1.0,1.0]
                        })
s=5.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch('bilinear',{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
