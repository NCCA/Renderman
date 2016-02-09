#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman
from Camera import *
from vector import *

from random import uniform as ru


def BuildField(wi,depth,inc,points,width,npoints) :
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
			pappend(0)
			pappend(zpos+ru(minus,plus))
			
			pappend(xpos+ru(minus,plus))
			pappend(0.0)
			pappend(zpos+ru(minus,plus))
			
			pappend(xpos+ru(minus,plus))
			pappend(0.0)
			pappend(zpos+ru(minus,plus))
		
			pappend(xpos+ru(minus,plus))
			pappend(0.0)#.3+ru(-0.1,0.1))
			pappend(zpos+ru(minus,plus))
		
			wappend(0.006)
			wappend(0.003)
			npappend(4)
			xpos+=inc
		zpos+=inc
	

def UpdateField(points,scale) :
	for i in range(0,len(points),12) :
		points[i+4]=scale
		points[i+7]=2*scale
		points[i+10]=5*scale

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

points=[]
width=[]
npoints=[]
dir=0
dircount=0
BuildField(1.5,2,0.1,points,width,npoints)
#BuildField(1,1,0.5,points,width,npoints)

offset=0.0
cam=Camera(Vector(0.1,0.4,2,1),Vector(0,0,0,1),Vector(0,1,0,0))
cam.fov=40

for frame in range(0,100) :

	filename = "__render" #"corn.%03d.rib" %(frame)
	print "processing ",frame
	# this is the begining of the rib archive generation we can only
	# make RI calls after this function else we get a core dump
	ri.Begin(filename)
	# ArchiveRecord is used to add elements to the rib stream in this case comments
	# note the function is overloaded so we can concatinate output
	ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
	ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
	ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
	ri.Declare("Light1" ,"string")
	ri.Declare("Light2" ,"string")
	

	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("growcorn.%03d.exr" %(frame), "file", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(720,576,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
	
	cam.Place(ri)
	
	# now we start our world
	ri.WorldBegin()
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,-0.03,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,-0.03,0], "float intensity": [1]})
	
	ri.Illuminate("Light1",1)
	ri.Illuminate("Light2",1)
	
	
	ri.TransformBegin()
	print offset
	

	offset+=0.001
	ri.Surface("hair")
	ri.Curves( "cubic",npoints,"nonperiodic",{ri.P:points, ri.WIDTH : width})
	UpdateField(points,offset)
	
	ri.TransformEnd()
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
