#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random,math
# import the python renderman library
import prman




	
def Scene(ri) :
	random.seed(25)
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Color([1,1,1])
	ri.Translate( 0,-1.0,0)
	ri.Rotate(-90,1,0,0)
	ri.Rotate(36,0,0,1)
	ri.Scale(0.4,0.4,0.4)
	ri.Surface("plastic")
	ri.Geometry("teapot")
	ri.AttributeEnd()
	ri.TransformEnd()
	face=[-0.1,-1,-3, 0.1,-1,-3,-0.1,-1,3, 0.1,-1,3]
	plank=-5.0
	
	ri.AttributeBegin()
	while (plank <=5.0) :
		ri.TransformBegin()
		ri.Color([random.uniform(0.35,0.4),random.uniform(0.1,0.025),0])
		c0=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		c1=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		ri.Surface("wood",{"Ks":[0.1],"point c0":c0,"point c1":c1,"float grain":random.randint(2,20)})
		ri.Translate(plank,0,0)
		ri.Patch("bilinear",{'P':face})
		ri.TransformEnd()
		plank=plank+0.206
	ri.AttributeEnd()

	
SpotFrom=[2,4,3]
SpotTo=[0,0,0]
SpotName="Spot1"
coneAngle=0.4

Spot2From=[2,4,-3]
Spot2To=[0,0,0]
Spot2Name="Spot2"
coneAngle2=0.3

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})



filename = "RayTrace.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')
ri.Clipping(1,10)

ri.Attribute("visibility", {"int diffuse" :1,
							"int specular": 1,
							"int transmission": 1})
							
							
ri.Attribute("trace",  {"int maxdiffusedepth" :[1], "int maxspeculardepth" : [2],
  						"int displacements" : [0] , "bias" : [.01],
  						"int samplemotion" : [0]})
 
							
							
							
							
							
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
ri.Declare(SpotName ,"string")

ri.Declare("Ambient" ,"string")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("RayTrace.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

ri.Translate(0,0,4)

# now we start our world
ri.WorldBegin()



ri.LightSource ("ambientlight",{ri.HANDLEID: "Ambient","intensity" :[0.05]}) 


ri.LightSource( "shadowspot", {ri.HANDLEID:SpotName,
				"point from" : SpotFrom, 
            	"point to" : SpotTo,
            	"float intensity" : [30],
            	"string shadowname" :"raytrace",
            	"float coneangle" : coneAngle,
            	"float conedeltaangle" : [0.05]})
  
ri.LightSource( "shadowspot", {ri.HANDLEID:Spot2Name,
				"point from" : Spot2From, 
            	"point to" : Spot2To,
            	"float intensity" : [30],
            	"string shadowname" :"raytrace",
            	"float coneangle" : coneAngle2,
            	"float conedeltaangle" : [0.05]})
Scene(ri)

ri.WorldEnd()

# and finally end the rib file
ri.End()
