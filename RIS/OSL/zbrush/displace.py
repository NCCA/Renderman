#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../../common')
from functions import drawTeapot
import Obj
from Camera import Camera
from Vec4 import Vec4
from Transformation import *
import random


ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" 
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("zbrush.exr", "it", "rgba")
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (10)
ri.ShadingRate(10)
ri.Integrator ("PxrPathTracer" ,"integrator")


# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
cam=Camera(Vec4(0,0.9,-3.9),Vec4(0,0.2,0),Vec4(0,1,0))
cam.place(ri)


# now we start our world
ri.WorldBegin()
#Lighting We need geo to emit light

"""
ri.TransformBegin()
ri.AttributeBegin()

lightTx=Transformation()
lightTx.setPosition(0,6,0)
lightTx.setRotation(90,0,0)
lightTx.setScale(10,10,10)
ri.ConcatTransform(lightTx.getMatrix())
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", "float exposure"  : [6],
                                       })
ri.Bxdf( "PxrDisney","bxdf", {  "color emitColor" : [ 1,1,1] })

ri.Geometry("rectlight")
ri.AttributeEnd()
ri.TransformEnd()
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
                                        "string rman__EnvMap" : ["../../meshes/Exterior1_Color.tx"]
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

# load mesh
troll=Obj.Obj("../../meshes/troll.obj")

tx=Transformation()


ri.Pattern("PxrTexture", "TrollColour",{ "string filename" : "../../meshes/TrollColour.tx"})
ri.Pattern("PxrTexture", "TrollSpecular",{ "string filename" : "../../meshes/TrollSpec.tx"})
ri.Pattern("PxrTexture", "TrollNMap",{ "string filename" : "../../meshes/TrollNormal.tx"})
ri.Pattern("PxrNormalMap", "TrollBump",{ "string filename" : "../../meshes/TrollNormal.tx", "float bumpScale" :[2]})

ri.Attribute ("trace" ,{"int displacements" : [ 1 ]})
ri.Attribute ("displacementbound", {"float sphere" : [10], "string coordinatesystem" : ["shader"]})

ri.Displacement("RMSDisplacement", {"reference vector displacementVector" : ["TrollBump:resultN"],
"float displacementAmount" : [0.5]})

ri.Bxdf( "PxrDisney","bxdf", {  "reference color baseColor" : ["TrollColour:resultRGB"] ,  "reference color subsurfaceColor" : ["TrollSpecular:resultRGB"], "float subsurface" : [0.4] , 
"float metallic" : [0.1],
"float specular" : [0.1],
"float roughness" : [0.3]

})

ypos=0.55
ri.TransformBegin()
tx.setPosition(-1,ypos,0)
tx.setRotation(0,-45,0)

ri.ConcatTransform(tx.getMatrix())
troll.Polygon(ri)
ri.TransformEnd();



ri.TransformBegin()
tx.setPosition(0,ypos,0)
tx.setRotation(0,45,0)
ri.ConcatTransform(tx.getMatrix())
troll.Polygon(ri)
ri.TransformEnd();


ri.TransformBegin()
tx.setPosition(1,ypos,0)
tx.setRotation(0,200,0)
ri.ConcatTransform(tx.getMatrix())
troll.Polygon(ri)
ri.TransformEnd()

# floor
ri.TransformBegin()

ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1,1,1],
                        "float roughness" : [ 0.2 ],

                        })
#ri.Bxdf( "PxrDiffuse","bxdf", {  "reference color diffuseColor" : ["colourChecker:resultRGB"] })

s=12.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
