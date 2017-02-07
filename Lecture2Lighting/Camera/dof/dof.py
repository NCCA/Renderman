#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman
from Camera import *
from vector import *


def Scene(ri) :
	ri.AttributeBegin()
	ri.Surface("texmap" ,{"string texname" : "ratGrid.tex","float maptype" : [0]})

	ri.TransformBegin()
	w=5.0 
	h=1.0
	d=5
	ri.Color([1,1,1])
	#ri.Surface("plastic")
	
	ri.Translate(0,-1,0)
	ri.TransformBegin()
	face=[-w,-h,-d,-w,h,d,w,-h,-d,w,h,d]								
	ri.Patch("bilinear",{'P':face})
	ri.TransformEnd()
	ri.TransformEnd()
	

	ri.TransformBegin()
	ri.Surface("texmap" ,{"string texname" : "grid.tex","float maptype" : [3]})
	#ri.Surface("plastic")
	ri.Rotate(-90,0,0,1)
	w=1.0 
	h=1.0
	d=5.0
	#ri.Surface("plastic")
	#ri.Translate(0,0,2)
	face=[-w,-h,d,-w,h,d,w,-h,d,w,h,d]
	ri.TransformBegin()
	ri.Scale(5,7,1)
	ri.Patch("bilinear",{'P':face})
	ri.TransformEnd()
	ri.TransformEnd()
	
	
	ri.Surface("plastic")

	ri.TransformBegin()
	ri.Color([1,0,0])
	ri.Translate(2,0,1)
	ri.Sphere(1.0,-1.0,0,360)
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Color([0,1,0])
	ri.Translate(0,0,0)
	ri.Sphere(1.0,-1.0,0,360)
	ri.TransformEnd()


	ri.TransformBegin()
	ri.Color([0,0,1])
	ri.Translate(-2,0,-1)
	ri.Sphere(1.0,-1.0,0,360)
	ri.TransformEnd()
	ri.AttributeEnd()
	
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})
cam=Camera(Vector(0.0,0.0,-6,1),Vector(0,0,0,1),Vector(0,1,0,0))
cam.fov=50
depth =2.5
cam.fstop=8
cam.focallength=1.0
cam.focaldistance=depth
for frame in range(1,30) :
	filename = "dof.%03d.rib" %(frame)
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
	ri.Declare("Ambient" ,"string")
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("dof.%03d.png" %(frame), "file", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	cam.Format(ri)

	
	cam.dof(ri)
	depth +=0.5
	cam.focaldistance=depth	
	# now we start our world
	ri.WorldBegin()
	ri.LightSource ("ambientlight",{ri.HANDLEID: "Ambient","intensity" :[0.5]}) 
	
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,-0.03,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,-0.03,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,-0.5,-1], "float intensity": [0.2]})
	
	ri.Illuminate("Light1",1)
	ri.Illuminate("Light2",1)
	ri.Illuminate("Light3",1)

	cam.Place(ri)
	Scene(ri)
	
	
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
