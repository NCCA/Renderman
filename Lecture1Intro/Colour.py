#!/usr/bin/python
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option('rib', {'string asciistyle': 'indented'})

filename = '__render' #'Colour.rib'
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('Colour.exr', 'it', 'rgba')
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
# now we start our world
ri.WorldBegin()

ri.Translate(0,0,5)
ri.Bxdf( 'PxrDiffuse','diffuse', 
{
'color diffuseColor' : [ 1.0, 0.0, 1.0]
})
ri.TransformBegin()
ri.Translate(-0.5,0,0)
ri.AttributeBegin()
ri.Bxdf( 'PxrDiffuse','diffuse', 
{
'color diffuseColor' : [ 0, 0, 1]
})

ri.Sphere(1,-1,1,360)
ri.AttributeEnd()
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(0.5,0,0)
ri.Sphere(1,-1,1,360)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
