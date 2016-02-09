#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "GeneralPolygon.rib"
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
ri.Display("GeneralPolygon.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 


# now we start our world
ri.WorldBegin()

ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,0,0], "float intensity": [1]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,0,0], "float intensity": [1]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,0,1], "float intensity": [1]})

ri.Illuminate("Light1",1)
ri.Illuminate("Light2",1)
ri.Illuminate("Light3",1)

ri.Translate(0,0,5)

ri.TransformBegin()

ri.Color([1,0,0])

points=[-2,-2,0,-2,2,0,2,2,0,2,-2,0,-1,-1,0,0,1,0,1,-1,0]
tx=[0,1, 0,0, 1,0, 1,1,  0.25,0.75, 0.5,0.25, 0.75,0.75]


ri.Surface("texmap",{"string texname":"ratGrid.tex","float maptype" :[3]})
ri.GeneralPolygon([4,3],{ri.P:points,ri.ST:tx})

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
