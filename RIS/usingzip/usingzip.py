#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
from Camera import *
from Transformation import *
from functions import drawTeapot
ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("rgb.exr", "it", "rgba")
ri.Format(1024,720,1)
#ri.Format(3840,2160,1)
# setup the raytrace / integrators
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (0.02)
ri.ShadingRate(0.1)

#ri.Integrator ("PxrDefault" , "integrator")
#ri.Integrator ("PxrVCM" ,"integrator")
#ri.Integrator ("PxrDirectlighting" ,"integrator")
ri.Integrator ("PxrPathTracer" ,"integrator")
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:44.43}) 
# DOF etc
ri.DepthOfField(16 ,3 ,120)
ri.Camera("camera",{ri.FOV: [44.43], "float natural" : [0.4], "float roll" : [6]})

# Front Cam
cam=Camera(Vec4(53.213,19.744,0.071),Vec4(0,5,0),Vec4(0,1,0))
# Top Cam
#cam=Camera(Vec4(0,50,0),Vec4(0,0,0),Vec4(0,0,1))
cam.place(ri)



# now we start our world
ri.WorldBegin()

#Lighting We need geo to emit light
"""
ri.AttributeBegin()
#ri.Rotate(45,0,1,0)
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", 
                                        "float exposure" : [15]
                                       })
#ri.Scale(2,2,2)
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color emitColor" : [ 1,1,1]
                        })


ri.TransformBegin()
ri.Translate(0.8,10,100)
ri.Rotate(180,1,0,0)
#ri.Scale(.1,.1,.1)
ri.Geometry("rectlight")
ri.TransformEnd()
ri.AttributeEnd()
"""

ri.AttributeBegin()

ri.Declare("areaLight" ,"string")

"""
# Temple Light Source
ri.AreaLightSource( "PxrStdEnvMapLight", {ri.HANDLEID:"areaLight", 
                                        "float exposure" : [0.4],
                                        "string rman__EnvMap" : ["temple.tx"]
                                      })
"""

"""
# Studio light source
ri.AreaLightSource( "PxrStdEnvMapLight", {ri.HANDLEID:"areaLight", 
                                        "float exposure" : [1.0],
                                        "string rman__EnvMap" : ["studio2.tx"]
                                      })
"""
# Outside light source
ri.AreaLightSource( "PxrStdEnvMapLight", {ri.HANDLEID:"areaLight", 
                                        "float exposure" : [1.0],
                                        "string rman__EnvMap" : ["Exterior1_Color.tx"]
                                      })

#ri.Bxdf( "PxrDisney","bxdf", {  "color emitColor" : [ 1,1,1] })

ri.TransformBegin()
lightTx=Transformation()
#lightTx.setPosition(10,10,10)
lightTx.setRotation(-90,0,0)
lightTx.setScale(12.5,12.5,12.5)
ri.ConcatTransform(lightTx.getMatrix())
ri.Geometry('envsphere')
ri.TransformEnd()
ri.AttributeEnd()




ri.TransformBegin()

ri.AttributeBegin()
#ri.Bxdf( "PxrDisney","bxdf", { "color baseColor" : [ .35, 0.49, 0.86] })
#ri.Bxdf( "PxrLMPlastic","bxdf", { "color diffuseColor" : [ .35, 0.49, 0.86] })



# set the pattern generation to be from our osl noise shader 
ri.Pattern("PxrOSL","noiseShader", { "string shader"  : "noise" , 
                                 "color Cin"  : [1.0 ,0.2,0.0],
                                "float scaleU" : [20],
                                 "float scaleV" : [30]

                                })
# now we are going to make a new pattern that changes the colour
# from the noise shader to a single float and extract the green channel
# mode==1
ri.Pattern ("PxrToFloat","noiseToFloat",{
		"reference color input" : ["noiseShader:Cout"],
                "int mode" : [1]
    })
ri.Bxdf( "PxrDisney","bxdf", { 
                                "reference color baseColor" : ["noiseShader:Cout"],
                                "reference float metallic" : ["noiseToFloat:resultF"]
                        })

"""
#Spots!
ri.Pattern("PxrOSL","distance", { "string shader"  : "distance" , 
                                     "float repeatU" : [25],  
                                     "float repeatV" : [25],  
                                     "color baseColour" : [1,1,1],
                                     "color spotColour" : [1,0,0],
                                     "float fuzz" : [0.08]                             
                                })
ri.Bxdf( "PxrDisney","bxdf", { "reference color baseColor" : ["distance:Cout"] })
"""

#Spots!
"""
ri.Pattern("PxrOSL","hole", { "string shader"  : "hole"   })
ri.Bxdf( "PxrDisney","bxdf", { "reference float presence" : ["hole:resultF"] })
"""



ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!shaderBall.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })
ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!cones.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })
ri.AttributeEnd()
# BAND
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.8, 0.8], 
                         "float metallic" : [0.2],
                          "float roughness" : [0],
                          "float specular" : [0.1]
                        })

ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!band.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })

ri.AttributeEnd()



# Inner Ball
ri.AttributeBegin()
"""
# Black
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.1, 0.1, 0.1],
                         "float roughness" : [0.2],
                          "float specular" : [0.1]
                        })
"""
# glowing red!
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.9, 0.0, 0.0], 
                        "color emitColor" : [1.0 , 0.0 , 0.0]
                        })

ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!innerBall.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })

ri.AttributeEnd()


ri.AttributeBegin()

ri.Bxdf( "PxrDisney","bxdf", { 
                          "color baseColor" : [ 1.0, 1.0, 1.0], 
                          "float metallic" : [1],
                          "float roughness" : [0],
                          "float specular" : [0.5]
                          })
ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!chromeBall.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })
drawTeapot(ri,x=19,y=0,z=-9,ry=-60,sx=1.2,sy=1.2,sz=1.2)

ri.AttributeEnd()

ri.AttributeBegin()

ri.Pattern("PxrTexture", "colourChecker",{ "string filename" : "checker.tx"})
ri.Bxdf( "PxrDisney","bxdf", { 
                        "reference color baseColor" : ["colourChecker:resultRGB"], 
                        })
ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!colChecker.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })
ri.AttributeEnd()

# Lambert Ball

ri.AttributeBegin()
#ri.Bxdf( "PxrDiffuse","bxdf", {   "color diffuseColor" : [.8,.8,.8] })
ri.Bxdf( "PxrLMPlastic","bxdf", { "color diffuseColor" : [ .8, 0.8, 0.8] })

ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!lambertBall.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })
drawTeapot(ri,x=14,y=0,z=-9,ry=-60,sx=1.2,sy=1.2,sz=1.2)

ri.AttributeEnd()

ri.Scale(2,2,2)
ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!signature.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })

# floor
# set the pattern generation to be from our osl check shader 

ri.Pattern("PxrOSL","checkShader", { "string shader"  : "simplecheck" ,  "float repeatCount" : [80],
"color Cin" : [0.5,0.5,0.5],
"color tileColour" : [0.4,0.4,0.4]})
ri.Bxdf( "PxrDisney","bxdf", {"reference color baseColor" : ["checkShader:Cout"]})


"""
# Image Texture
ri.Pattern("PxrTexture", "colourChecker",{ "string filename" : "ratGrid.tx"})

ri.Bxdf( "PxrDisney","bxdf", { 
                        "reference color baseColor" : ["colourChecker:resultRGB"], 
                        })

"""
"""
# Solid colour
ri.Bxdf( "PxrDisney","bxdf", {   "color baseColor" : [ 1.0,1.0,1.0] })
"""
#ri.Scale(2,2,2)
ri.Procedural2( ri.Proc2DelayedReadArchive, ri.SimpleBound  , {"string filename" : ["shaderBall.zip!floor.rib"] , "float[6] __bound" : [-2 ,2, 0 ,2, -2 ,2] })

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
