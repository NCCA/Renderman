#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman

ri = prman.Ri() # create an instance of the RenderMan interface

ri.Option("rib", {"string asciistyle": "indented"})
for frame in range(0,1) :
	
	filename = "Obj2Rib.%03d.rib" %(frame)
	print "Rendering Frame",frame
	# this is the begining of the rib archive generation we can only
	# make RI calls after this function else we get a core dump
	ri.Begin("__render")
	# ArchiveRecord is used to add elements to the rib stream in this case comments
	# note the function is overloaded so we can concatinate output
	ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
	ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
	ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
	ri.Attribute("displacementbound",{ri.COORDINATESYSTEM:["object"],"uniform float sphere":[2]})
	ri.Declare("Light1" ,"string")
	ri.Declare("Light2" ,"string")
	ri.Declare("Light3" ,"string")
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("Obj2Rib.%03d.exr" %(frame), "framebuffer", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(720,576,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:45}) 
	#ri.ShadingRate([1])
	#ri.ShadingInterpolation("smooth")
	ri.ShadingInterpolation("smooth")
	
	ri.ShadingRate( [0.1])
	ri.PixelSamples( 48,48)
	ri.PixelFilter( ri.GAUSSIAN ,2.0, 1.0)
	# now we start our world
	ri.WorldBegin()
	
	ri.LightSource( "pointlight", {ri.HANDLEID:"Light1", "point from":[0,0,2], "float intensity": [0.1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light2", "point to":[-1,0,0], "float intensity": [1]})
	ri.LightSource( "distantlight", {ri.HANDLEID:"Light3", "point to":[1,0,0], "float intensity": [2]})
	
	ri.LightSource( "ambientlight", {ri.HANDLEID:"Light4", "float intensity": [0.2]})
	
	ri.Illuminate("Light1",1)
	ri.Illuminate("Light2",1)
	ri.Illuminate("Light3",1)
	ri.Color([1,1,1])
	
	ri.Displacement(  "ZBrushDisplacement" ,{"float Km": [0.35],"string displace_map" : "CaveTrollDisp.tx", "float swidth": [0.0001],"float twidth": [0.0001],"float samples": [400.000], })
	ri.Surface("plastic",{"Ks":[0]},"Kd",[0.5])
	ri.Translate(0,0,13)
	ri.TransformBegin()
	ri.Translate(0,-6,-8)
	ri.Scale(0.08,0.08,0.08)
	ri.Rotate(40,0,1,0)
	ri.ReadArchive("CaveTroll2.rib")
	ri.TransformEnd()
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
