#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman
from Obj import *

objFile="../Models/clubbot.obj"

obj=Obj(objFile,5)
particles=[]
Width=[]
for i in range(0,len(obj.verts)) :
	for x in range(0,len(obj.verts[i])) :
		particles.append(obj.verts[i][x])
for i in range(0,len(particles)/3) :
	Width.append(0.1)		


ri = prman.Ri() # create an instance of the RenderMan interface

ri.Option("rib", {"string asciistyle": "indented"})

for frame in range(0,60) :

	filename = "Particle.%03d.rib" %(frame)
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
	ri.Declare("Light3" ,"string")
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("Particle.%03d.exr" %(frame), "file", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(720,575,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
	
	
	# now we start our world
	ri.WorldBegin()
	
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,0,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,0,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,0,1], "float intensity": [0.2]})
	
	ri.Illuminate("Light1",1)
	ri.Illuminate("Light2",1)
	ri.Illuminate("Light3",1)
	#xmin,xmax,ymin,ymax,zmin,zmax= obj.getExtents()
	
	ri.Translate(0,-8,22)
	
	ri.TransformBegin()
	ri.Surface("texmap",{"string texname":"../Models/clubbot.tx","float maptype" :[3]})
	
	ri.Rotate(90,0,1,0)
	obj.Polygon(ri,5)
	ri.AttributeBegin()
	ri.Color([1,1,1])
	ri.Surface("plastic")
	ri.Points({ri.P:particles,"varying float width":Width})
	ri.AttributeEnd()
	ri.TransformEnd()
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
	#update the particles
	for i in range(0,len(particles),3) :
		particles[i]=particles[i]+0.1
