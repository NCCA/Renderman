#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "runprogram.rib"
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
ri.Display("runprogram.exr", "file", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:60}) 

ri.Identity()
ri.ConcatTransform( [1.0,0.0,0.0,0.0,0.0,0.9,-0.4,0.0,0.0,0.4,0.9,0.0,-0.0,-0.0,16.925824,1.0])

# now we start our world
ri.WorldBegin()


ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,0.03,0], "float intensity": [1]})
ri.LightSource( "pointlight", {ri.HANDLEID:"Light2", "point from":[0,2.0,0], "float intensity": [2]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,0,-1], "float intensity": [2]})

ri.Illuminate("Light1",1)
ri.Illuminate("Light2",1)
ri.Illuminate("Light3",1)

ri.TransformBegin()
ri.Color([1, 0, 0])
ri.Translate( 0 ,-1 ,0) 

# param width height depth Case Height Rotation Angle
program="Procedural \"RunProgram\" [\"spiral.py\" \"1 0.2 0.35 20 5\"] [-5 5 -5 5 -35 35]\n"
ri.ArchiveRecord(ri.VERBATIM,program)

ri.TransformEnd()
ri.TransformBegin()
ri.Color([1, 1 ,1])
ri.Translate( -6 ,-1, 0)	
# param width height depth Case Height Rotation Angle
program="Procedural \"RunProgram\" [\"spiral.py\" \"5 0.5 1.5 10 15\"] [-5 5 -5 5 -35 35]\n"
ri.ArchiveRecord(ri.VERBATIM,program)

ri.TransformEnd()

ri.TransformBegin()
ri.Color([1, 0, 1])
ri.Translate( 6, -1, 0)
# param width height depth Case Height Rotation Angle
program="Procedural \"RunProgram\" [\"spiral.py\" \"2 0.3 0.3 10 12\"] [-5 5 -5 5 -35 35]\n"
ri.ArchiveRecord(ri.VERBATIM,program)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
