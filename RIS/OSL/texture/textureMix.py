#!/usr/bin/python
import prman,os,subprocess
# import the python functions
import sys
sys.path.append('../../common')
from functions import drawTeapot
from Camera import *

'''
function to check if shader exists and compile it, we assume that the shader
is .osl and the compiled shader is .oso If the shader source is newer than the
compiled shader we will compile it. It also assumes that oslc is in the path.
'''
def checkAndCompileShader(shader) :
	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
		print 'compiling shader %s' %(shader)
		try :
			subprocess.check_call(['oslc', shader+'.osl'])
		except subprocess.CalledProcessError :
			sys.exit('shader compilation failed')
		 

checkAndCompileShader('textureMix')
checkAndCompileShader('textureRand')

ri = prman.Ri() # create an instance of the RenderMan interface

filename = '__render' 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('rgb.exr', 'it', 'rgba')
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider('raytrace' ,{'int incremental' :[1]})
ri.PixelVariance (0.02)
ri.ShadingRate(20)

ri.Integrator ('PxrPathTracer' ,'integrator')
ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
ri.Option( 'statistics', {'endofframe' : [ 1 ] })
ri.Attribute ('trace' ,{'int displacements' : [ 1 ]})
ri.Attribute ('displacementbound', {'float sphere' : [20], 'string coordinatesystem' : ['shader']})

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
ri.Declare('areaLight' ,'string')
# position light
ri.Translate(0.0,1.5,3)
ri.Rotate(180,1,0,0)
ri.Rotate(-30,1,0,0)
# add geometry for debug (off screen here)
ri.Bxdf( 'PxrDisney','bxdf', {'color emitColor' : [ 1,1,1] })
ri.Geometry('rectlight')
# enable light
ri.Light( 'PxrRectLight', 'areaLight',{'float exposure' : [3] })
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################
# first teapot

ri.Pattern('textureMix','textureMix', 
{ 
  'color cin'  : [.2, .5 ,.8], 
  'string filename' : 'nccatransp.tx',
})


ri.Bxdf( 'PxrDisney','bxdf', 
{                         
  'reference color baseColor' : [ 'textureMix:resultRGB']
})


# ri.Displace('PxrDisplace','displaceTexture' ,
# {   
#   'reference float dispScalar' : ['textureMix:resultA'], 
#   'uniform float dispAmount' : [0.02],
#   'int enabled' : [1]
# })

ri.AttributeBegin()
      

drawTeapot(ri,x=-1,ry=-45)
ri.AttributeEnd()

# second teapot
drawTeapot(ri,ry=-45)

# third teapot
drawTeapot(ri,x=1,ry=-45)
# floor
ri.AttributeBegin()

ri.Pattern('textureRand','textureRand', 
{ 
  'color cin'  : [1.0, 1.0 ,1.0], 
  'float scaleS' : [40],
  'float scaleT' : [40],
  'string filename' : 'nccatransp.tx',
})


ri.Bxdf( 'PxrDisney','bxdf', 
{                         
  'reference color baseColor' : [ 'textureRand:resultRGB']
})


# ri.Displace('PxrDisplace','displaceTexture' ,
# {   
#   'reference float dispScalar' : ['textureRand:resultA'], 
#   'uniform float dispAmount' : [0.02],
#   'int enabled' : [1]
# })


ri.TransformBegin()
s=5.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch('bilinear',{'P':face})

ri.TransformEnd()
ri.AttributeEnd()


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
