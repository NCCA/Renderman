#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman



def Scene(ri) :

	ri.SolidBegin("intersection")
    
	ri.SolidBegin("primitive")                                                                                                                                                              
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Color([1,1,1])
	ri.Translate( 0,-1.0,0)
	ri.Surface("plastic")
	ri.Sphere(1.0,-1,1,360)
	
	ri.Translate(0,-0.1,0)
	ri.Sphere(1.0,-1,1,360)

	ri.AttributeEnd()
	ri.TransformEnd()
	ri.SolidEnd()
	
	
	ri.SolidBegin("primitive")                                                                                                                                                              

	for i in range(0,360,20) :
		ri.TransformBegin()
		ri.Rotate(i,0,1,0)	
		ri.Translate(-0.6,-0.3,0)
		ri.Scale(0.1,0.1,0.1)
		ri.Sphere(1,-1,1,360)
		ri.TransformEnd()
	ri.SolidEnd()
	
	ri.SolidEnd()
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "CSGIntersect.rib"
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
ri.Display("CSGIntersect.exr", "file", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 



# now we start our world
ri.WorldBegin()


ri.LightSource( "distantlight", {ri.HANDLEID:"Light1", "point to":[1,-0.03,0], "float intensity": [1]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,-0.03,0], "float intensity": [1]})
ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[0,-0.5,-1], "float intensity": [0.2]})

ri.Illuminate("Light1",1)
ri.Illuminate("Light2",1)
ri.Illuminate("Light3",1)



ri.Translate(0,0.2,2)
ri.TransformBegin()
ri.Rotate(-45,1,0,0)
Scene(ri)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
