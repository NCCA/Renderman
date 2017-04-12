#!/usr/bin/python
import prman
# import the python functions
import sys,os.path,subprocess
sys.path.append('../../../common')
from functions import drawTeapot
from Camera import *

"""
function to check if shader exists and compile it, we assume that the shader
is .osl and the compiled shader is .oso If the shader source is newer than the
compiled shader we will compile it. It also assumes that oslc is in the path.
"""
def checkAndCompileShader(shader) :
	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
		print "compiling shader %s" %(shader)
		try :
			subprocess.check_call(["oslc", shader+".osl"])
		except subprocess.CalledProcessError :
			sys.exit("shader compilation failed")
		 

checkAndCompileShader('noise')
ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("rgb.exr", "it", "rgba")
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (0.02)
ri.ShadingRate(20)


ri.Integrator ("PxrPathTracer" ,"integrator")

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
cam=Camera(Vec4(-2,2.2,3),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)



# now we start our world
ri.WorldBegin()

#Lighting We need geo to emit light
ri.AttributeBegin()

#ri.Rotate(45,0,1,0)
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", 
                                        "float exposure" : [4]
                                       })
#ri.Scale(2,2,2)
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color emitColor" : [ 1,1,1]
                        })

"""
ri.TransformBegin()
ri.Translate(1.8,0.9,2.3)
ri.Sphere(0.3, -0.3, 0.3 ,360)
ri.TransformEnd()
"""
ri.TransformBegin()
ri.Translate(0.8,1.3,2)
ri.Rotate(180,1,0,0)
ri.Scale(.1,.1,.1)
ri.Geometry("rectlight")
ri.TransformEnd()


ri.AttributeEnd()

# set the pattern generation to be from our osl noise shader 
ri.Pattern("PxrOSL","noiseShader", { "string shader"  : "noise" , 
                                 "color Cin"  : [1.0 ,0.2,0.0]
                                })
# now we are going to make a new pattern that changes the colour
# from the noise shader to a single float and extract the green channel
# mode==1
ri.Pattern ("PxrToFloat","noiseToFloat",{
		"reference color input" : ["noiseShader:Cout"],
                "int mode" : [1]
    })

# first teapot
ri.AttributeBegin()
# the colour from the shader is driven by noise, metallic by the noise green channel via the noiseToFloat 
ri.Bxdf( "PxrDisney","bxdf", { 
                                "reference color baseColor" : ["noiseShader:Cout"],
                                "reference float metallic" : ["noiseToFloat:resultF"]
                        })
drawTeapot(ri,x=-1,ry=-45)
ri.AttributeEnd()
ri.Pattern("PxrOSL","noiseShader", { "string shader"  : "noise" , 
                                 "color Cin"  : [0.0 ,1.0,0.1],
                                 "float scaleU" : [20],
                                 "float scaleV" : [30]
                                })
# second teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                                "reference color baseColor" : ["noiseShader:Cout"]
                        })
drawTeapot(ri,ry=-45)
ri.Pattern("PxrOSL","noiseShader", { "string shader"  : "noise" , 
                                 "color Cin"  : [0.0 ,0.0,1.0],
                                  "float scaleU" : [54],
                                 "float scaleV" : [54]
                                })
# third teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                                "reference color baseColor" : ["noiseShader:Cout"]
                        })
drawTeapot(ri,x=1,ry=-45)
# floor
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1.0,1.0,1.0]
                        })
s=5.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
