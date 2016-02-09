#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random,math
# import the python renderman library
import prman


	
def Scene(ri) :
	
	

	ri.TransformBegin()
	ri.Translate( 0, -0.9, 0)
	ri.Scale( 1 ,0.4, 1)
	ri.Surface("AOVplastic",{ "color SurfaceColor": [0,0,1],"color Transparency" :[1, 1 ,1],"float Ka" : [0.1],"float Kd": [0.5],"color Specularcolor" :[1, 1, 1]})

	ri.Patch( "bilinear",{ "P" : [-0.5, -0.5, 0.5,-0.5, 0.5 ,0.5 ,0.5, -0.5, 0.5 ,0.5, 0.5, 0.5] })      
	ri.Patch( "bilinear",{ "P" :  [-0.5 ,-0.5 ,-0.5 ,-0.5 ,0.5, -0.5, 0.5 ,-0.5, -0.5, 0.5 ,0.5 ,-0.5] })  
	ri.Patch( "bilinear",{ "P" :  [-0.5 ,-0.5 ,-0.5 ,-0.5, 0.5 ,-0.5 ,-0.5 ,-0.5 ,0.5 ,-0.5, 0.5 ,0.5] })  
	ri.Patch( "bilinear",{ "P" :  [0.5 ,-0.5 ,-0.5 ,0.5 ,0.5 ,-0.5 ,0.5 ,-0.5 ,0.5 ,0.5 ,0.5, 0.5] })     
	ri.Patch( "bilinear",{ "P" :  [0.5, -0.5, 0.5 ,0.5 ,-0.5, -0.5, -0.5 ,-0.5 ,0.5, -0.5 ,-0.5, -0.5] })  
	ri.Patch( "bilinear",{ "P" :  [0.5, 0.5, 0.5 ,0.5 ,0.5, -0.5, -0.5 ,0.5 ,0.5 ,-0.5 ,0.5 ,-0.5] })
	ri.TransformEnd()
	
	ri.TransformBegin()
	ri.Translate( 0.5, -1.0, -1.5)
	ri.Scale (0.2 ,0.2 ,0.2)
	ri.Rotate (-90, 1 ,0 ,0)
	ri.Rotate (55, 0, 0, 1)
	ri.Surface("AOVplastic",{ "color SurfaceColor": [1,0,0],"color Transparency" :[1, 1 ,1],"float Ka" : [0.1],"float Kd": [0.5],"color Specularcolor" :[1, 1, 1]})

	ri.Geometry ("teapot")
	ri.TransformEnd()
	
	ri.TransformBegin()
	ri.Translate( 0, -0.7, 0)
	ri.Scale( 0.2, 0.2, 0.2)
	ri.Rotate( -90, 1 ,0 ,0)
	ri.Rotate( 55, 0, 0, 1)
	ri.Surface("AOVplastic",{ "color SurfaceColor": [1,1,1],"color Transparency" :[1, 1 ,1],"float Ka" : [0.1],"float Kd": [0.5],"color Specularcolor" :[1, 1, 1]})

	ri.Geometry( "teapot")
	ri.TransformEnd()
	ri.TransformBegin()
	ri.Surface("AOVplastic",{ "color SurfaceColor": [1,1,0],"color Transparency" :[0.5, 0.5 ,0.5],"float Ka" : [0.1],"float Kd": [0.5],"color Specularcolor" :[1, 1, 1]})
	
	ri.Translate( 1.3, -0.5 ,.2)
	ri.Rotate( 90, 1, 0, 0)
	ri.Scale( 0.2, 0.2, 1.4)
	ri.Cylinder( 1, -0.5, 0.5, 360) 
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Opacity([1,1,1])
	ri.Translate( 1.3, 0.2, .2)
	ri.Rotate( 90, 1 ,0 ,0)
	ri.Scale( 0.2, 0.2, 2)
	ri.Disk( 0, 1 ,360)
	ri.TransformEnd()
	
	
	
	random.seed(25)
	face=[-0.1,-1,-3, 0.1,-1,-3,-0.1,-1,3, 0.1,-1,3]
	plank=-5.0
	
	ri.AttributeBegin()
	while (plank <=5.0) :
		ri.TransformBegin()
		ri.Color([random.uniform(0.35,0.4),random.uniform(0.1,0.025),0])
		ri.Surface("AOVplastic",{ "color SurfaceColor": [0.4,0.4,0.4],"color Transparency" :[1, 1 ,1],"float Ka" : [0.1],"float Kd": [0.5],"color Specularcolor" :[1, 1, 1]})
		ri.Translate(plank,0,0)
		ri.Patch("bilinear",{'P':face})
		ri.TransformEnd()
		plank=plank+0.206
	ri.AttributeEnd()

	
prman.Init(["-progress"])  # a list of string arguments, same as prman executable	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

Pl1=[3.2,-0.6,-2.5]
Pl2=[3.2,0.6,-2.5]
Pl3=[3.0,-0.6,2.0]
Pl4=[3.0,0.6,2.0]



To=[0,0,0]
coneAngle=0.4

SpotName="Spot1"

Spot2Name="Spot2"

Spot3Name="Spot3"

Spot4Name="Spot4"

filename = "AreaLight.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render") #filename)
ri.Clipping(0.1,20)

# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
ri.Declare("AreaLight" ,"string")

ri.Declare("Ambient" ,"string")

ri.DisplayChannel( "color Oambient")
ri.DisplayChannel("color Oreflect")
ri.DisplayChannel("color Ospecular")
ri.DisplayChannel("color Odiffuse")
ri.DisplayChannel("color Oopacity")
ri.DisplayChannel("color Oid")
ri.DisplayChannel("color OwsNormal")
ri.DisplayChannel("color OwsCamera")
ri.DisplayChannel("color OwsPtPos")
ri.DisplayChannel("color Obounce")



# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format

ri.Display( "Beauty.0001.exr", "openexr" ,"rgba", { "string filter": ["separable-catmull-rom"],"float[2] filterwidth" : [2 ,2],"int[4] quantize" : [0, 0, 0 ,0],"float dither": [0],"float[2] exposure" :[1, 1]}) 

#ri.Display("BeautyPass.exr", "file", "rgba")
ri.Display( "+Oambient.0001.exr", "openexr" ,"Oambient" ,{"int[4] quantize" :[0, 0 ,0, 0], "float dither": [0]})
ri.Display( "+Oreflect.0001.exr" ,"openexr" ,"Oreflect" ,{"int[4] quantize" :[0, 0, 0 ,0], "float dither" :[0]})
ri.Display( "+Ospecular.0001.exr" ,"openexr" ,"Ospecular" ,{"int[4] quantize" :[0 ,0 ,0 ,0], "float dither": [0]})
ri.Display( "+Odiffuse.0001.exr" ,"openexr" ,"Odiffuse" ,{"int[4] quantize" :[0, 0 ,0 ,0], "float dither": [0]})
ri.Display( "+Oopacity.0001.exr" ,"openexr" ,"Oopacity" ,{"int[4] quantize" :[0 ,0 ,0 ,0] ,"float dither" :[0]})
ri.Display( "+OwsNormal.0001.exr", "openexr", "OwsNormal",{ "int[4] quantize": [0 ,0 ,0, 0], "float dither": [0]})
ri.Display( "+OwsCamera.0001.exr", "openexr", "OwsCamera" ,{"int[4] quantize" :[0, 0 ,0 ,0], "float dither" :[0]})
ri.Display( "+OwsPtPos.0001.exr" ,"openexr" ,"OwsPtPos" ,{"int[4] quantize" :[0, 0 ,0 ,0], "float dither" :[0]})
ri.Display( "+Obounce.0001.exr" ,"openexr" ,"Obounce" ,{"int[4] quantize": [0, 0 ,0 ,0], "float dither" :[0]})

# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
ri.ShadingRate(8)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# top view
#ri.Translate(0,0,6)
#ri.Rotate(-90,1,0,0)
#close 
ri.Translate( 0 ,0.0, 3)
ri.Rotate (-10 ,1, 0 ,0)
ri.Rotate( 35 ,0 ,1 ,0)

"""
#normal view
ri.Translate(0,0,4)
"""
# now we start our world
ri.WorldBegin()

SpotFrom=[2,4,3]
SpotTo=[0,0,0]
SpotName="Spot1"
coneAngle=0.4

Spot2From=[2,4,-3]
Spot2To=[0,0,0]
Spot2Name="Spot2"
coneAngle2=0.3
ri.Attribute("visibility", {"int diffuse" :1,
							"int specular": 1,
							"int transmission": 1})
							
							
ri.Attribute("trace",  {"int maxdiffusedepth" :[1], "int maxspeculardepth" : [2],
  						"int displacements" : [0] , "bias" : [.01],
  						"int samplemotion" : [0]})
 
							
							
							
		
ri.LightSource ("ambientlight",{ri.HANDLEID: "Ambient","intensity" :[0.1]}) 


ri.AttributeBegin()
ri.Surface("defaultsurface")
ri.AttributeEnd()

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
