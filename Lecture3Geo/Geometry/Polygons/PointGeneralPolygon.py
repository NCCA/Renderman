#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "PointGeneralPolygon.rib"
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
ri.Display("PointsGeneralPolygon.exr", "file", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 


# now we start our world
ri.WorldBegin()

ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,0,0], "float intensity": [2]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,0,0], "float intensity": [2]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,0,0], "float intensity": [2]})

ri.Illuminate("Light1",1)
ri.Illuminate("Light2",1)
ri.Illuminate("Light3",1)

ri.Translate(0,-0.5,2)

ri.TransformBegin()
ri.Rotate(45,1,1,0)
ri.Color([1,0,0])


points=[0,0,1,
		0,1,1,
		0,2,1,
		0,0,0,
		0,1,0,
		0,2,0,
		0,0.25,0.5,
		0,0.75,0.75,
		0,0.75,0.25,
		0,1.25,0.5,
		0,1.75,0.75,
		0,1.75,0.25]

npolys=[2,2]		
nvertices=[4,3,4,3]
PolyVerts=[0,1,4,3,6,7,8,1,2,5,4,9,10,11]

ri.Surface("plastic")
ri.PointsGeneralPolygons(npolys,nvertices,PolyVerts,{ri.P:points})

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()