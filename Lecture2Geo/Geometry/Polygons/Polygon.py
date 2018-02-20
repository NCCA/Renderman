#!/usr/bin/python
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option('rib', {'string asciistyle': 'indented'})

filename = 'Polygon.rib'
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('Polygon.exr', 'it', 'rgba')
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# now we start our world
ri.WorldBegin()


ri.Translate(0,0,3)

ri.TransformBegin()

ri.Pattern('PxrTexture', 'ratGrid',
{ 
  'string filename' : 'ratGrid.tex' ,
  'int invertT' : [0]
})

ri.Bxdf( 'PxrDiffuse','diffuse', 
{
  'reference color diffuseColor'  : ['ratGrid:resultRGB']
})

points=[-1,-1,0,0,1,0,1,-1,0]
normals=[0,0,-1,0,0,-1,0,0,-1]
tx=[0,1,0.5,0,1,1]
ri.Polygon({ri.P:points,ri.N:normals,ri.ST:tx})

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
