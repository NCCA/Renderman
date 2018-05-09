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
ri.Pattern('PxrTexture', 'logo',
{ 
  'string filename' : 'nccatransp.tx',
  'int invertT' : [0]

})
ri.Pattern('PxrMix','mixer',
{
	'color color1' : [.2, .5 ,.8], 
	'reference color color2' : ['logo:resultRGB'], 
	'reference float mix' : ['logo:resultA'] 
})

ri.Bxdf( 'PxrDisney','bxdf', 
{                         
  'reference color baseColor' : [ 'mixer:resultRGB']
})


ri.Bxdf( 'PxrDisney','bxdf', 
{                         
  'reference color baseColor' : [ 'mixer:resultRGB']
})


ri.Displace('PxrDisplace','displaceTexture' ,
{   
  'reference float dispScalar' : ['logo:resultA'], 
  'uniform float dispAmount' : [0.02],
  'int enabled' : [1]
})

ri.AttributeBegin()
      

drawTeapot(ri,x=-1,ry=-45)
ri.AttributeEnd()

# second teapot
drawTeapot(ri,ry=-45)

# third teapot
drawTeapot(ri,x=1,ry=-45)
# floor
ri.AttributeBegin()


ri.Pattern('PxrTileManifold','tileManifold',
{
	'int numTextures' : [20], 
	'int textureOrder' : [1], 
	'float angle' : [45], 
	'float scaleS' : [20], 
	'float scaleT' : [20], 
	'int invertT' : [0], 
  'int randomOrientation' : [1],
  'float randomExtraSeed' : [0.12]

})

ri.Pattern('PxrTexture', 'logorepeat',
{ 
  'string filename' : 'nccatransp.tx',
  'int invertT' : [0],
  'reference struct manifold' : ['tileManifold:result']


})
ri.Pattern('PxrMix','mixerrepeat',
{
	'color color1' : [1.0,1.0,1.0], 
	'reference color color2' : ['logorepeat:resultRGB'], 
	'reference float mix' : ['logorepeat:resultA'] 
})

ri.Bxdf( 'PxrDisney','bxdf', 
{                         
  'reference color baseColor' : [ 'mixerrepeat:resultRGB']
})
ri.Displace('PxrDisplace','displaceTexture' ,
{   
  'reference float dispScalar' : ['logorepeat:resultA'], 
  'uniform float dispAmount' : [0.02],
  'int enabled' : [1]
})

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
