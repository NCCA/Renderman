#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "InlineArchive.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)

ri.ArchiveBegin("Wave")
ri.Rotate(90,1,0,0)
ri.Sphere(0.030303,-0.030303,0,360) 
ri.Torus(0.0606061,0.030303,0,180,360) 
ri.Torus(0.121212,0.030303,180,360,360) 
ri.Torus(0.181818,0.030303,0,180,360) 
ri.Torus(0.242424,0.030303,180,360,360) 
ri.Torus(0.30303,0.030303,0,180,360) 
ri.Torus(0.363636,0.030303,180,360,360) 
ri.Torus(0.424242,0.030303,0,180,360)
ri.Torus(0.484848,0.030303,180,360,360) 
ri.Torus(0.545455,0.030303,0,180,360)
ri.Torus(0.606061,0.030303,180,360,360) 
ri.Torus(0.666667,0.030303,0,180,360)
ri.Torus(0.727273,0.030303,180,360,360) 
ri.Torus(0.787879,0.030303,0,180,360) 
ri.Torus(0.848485,0.030303,180,360,360) 
ri.ArchiveEnd()

#ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))


# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("InlineArchive.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 


# now we start our world
colours ={
	"red":[1,0,0],
	"white":[1,1,1],
	"green":[0,1,0],
	"blue":[0,0,1],
	"black":[0,0,0],
	"yellow":[1,1,0]
	}


# start our world
ri.WorldBegin()
ri.Translate(0,0,10) #move the global view position
ri.TransformBegin()
ri.Rotate(30,1,0,0)
ri.Color(colours["red"])
ri.Attribute ("identifier",{"name": "Wave1"})
ri.ReadArchive("Wave")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30,1,0,0)
ri.Color(colours["green"]) 
ri.Translate(2.2,0,0)
ri.Attribute( "identifier",{ "name" :"Wave2"})
ri.ReadArchive("Wave")
ri.TransformEnd()
ri.TransformBegin()
ri.Rotate(30,1,0,0)
ri.Color(colours["blue"])
ri.Translate(-2.2,0,0)
ri.Attribute("identifier",{ "name" : "Wave3"})
ri.ReadArchive("Wave")
ri.TransformEnd()
#end our world

ri.WorldEnd()
# and finally end the rib file
ri.End()
