#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import time,random
# import the python renderman library
import prman

from random import uniform as ru


def buildField(wi,depth,inc,points,width,npoints) :
	xmin=-wi/2.0
	xmax=wi/2.0
	zmin=-depth/2.0
	zmax=depth/2.0
	pappend=points.append
	wappend=width.append
	npappend=npoints.append
	random.seed(1)
	ru=random.uniform
	zpos=zmin
	plus=0.1
	minus=-0.1
	while(zpos < zmax ) :
		xpos=xmin
		while (xpos < xmax) :
			pappend(xpos+ru(minus,plus))
			pappend(0) # z pos 1
			pappend(zpos+ru(minus,plus))
			
			pappend(xpos+ru(minus,plus))
			pappend(0.2) # z pos 2
			pappend(zpos+ru(minus,plus))
			
			pappend(xpos+ru(minus,plus))
			pappend(0.4) # z pos 3
			pappend(zpos+ru(minus,plus))
		
			pappend(xpos+ru(minus,plus))
			pappend(0.8+ru(-0.1,0.1)) # final z pos with random
			pappend(zpos+ru(minus,plus))
		
			wappend(0.006)
			wappend(0.003)
			npappend(4)
			xpos+=inc
		zpos+=inc
	


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

points=[]
width=[]
npoints=[]
dir=0
dircount=0
#BuildField(1.5,0.1,0.01,points,width,npoints)
buildField(14,14,0.2,points,width,npoints)

filename = "__render" #"corn.%03d.rib" %(frame)
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)
ri.ShadingRate(0.2)
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("MultiCurce" , "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(1024,720,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:40}) 
# now we start our world
ri.WorldBegin()
ri.Translate(0,0,10)
ri.Rotate(-20,1,0,0)

ri.TransformBegin()
ri.Curves( "cubic",npoints,"nonperiodic",{ri.P:points, ri.WIDTH : width})
ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
