#!/usr/bin/python
import prman

from random import uniform as ru

ri = prman.Ri() # create an instance of the RenderMan interface

filename = 'Points.rib'
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

ri.Option('searchpath', {'string shader': ['../../../Lecture1Intro/']})

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('Points.exr', 'it', 'rgba')
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 


# now we start our world
ri.WorldBegin()

ri.Translate(0,0,4)

ri.TransformBegin()

points=[]
width=[]
colour=[]
normals=[]
# get a pointer to the append method as it is faster than calling it
# each time
pappend=points.append
wappend=width.append
cappend=colour.append
nappend=normals.append
# ru is random.uniform brought in by the import statement above
for i in range(0,2000) :
	for ix in range(0,3) :
		cappend(ru(0,1))
		pappend(ru(-2,2))
		nappend(ru(0,1))	
	wappend(ru(0.01,0.2))
	
ri.Pattern( 'colour', 'colourShader')
ri.Bxdf( 'PxrDiffuse','bxdf', 
{
  'reference color diffuseColor' : ['colourShader:Cout']
})

ri.Points({ri.P:points,ri.CS:colour,ri.WIDTH:width,ri.N:normals})

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
