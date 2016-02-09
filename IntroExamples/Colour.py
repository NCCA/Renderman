#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "__render" #"Colour.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Colour.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# now we start our world
ri.WorldBegin()
colours ={
	"red":[1,0,0],
	"white":[1,1,1],
	"green":[0,1,0],
	"blue":[0,0,1],
	"black":[0,0,0],
	"yellow":[1,1,0]
	}


ri.Translate(0,0,5)
ri.Color([1,0,1])
ri.Opacity([1,1,1])
ri.TransformBegin()
ri.Translate(-0.5,0,0)
ri.AttributeBegin()
ri.Color(colours["blue"])
ri.Opacity([0.2,0.2,0.2])
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
