#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
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
ri.Display("simple.exr", "it", "rgba")
ri.Format(1024,720,1)

# setup the raytrace / integrators
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (0.01)

ri.Integrator ("PxrVCM" ,"integrator")
#ri.Integrator ("PxrDirectlighting" ,"integrator")
ri.Integrator ("PxrPathTracer" ,"integrator")
#ri.Integrator ("PxrVisualizer" ,"integrator", {"string style" : "bxdf"})


# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:30}) 
# Simple translate for our camera
cam=Camera(Vec4(0,2,-10),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)


# now we start our world
ri.WorldBegin()
#Lighting We need geo to emit light
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
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color emitColor" : [ 1,1,1]
                        })

ri.Geometry("rectlight")
ri.AttributeEnd()
ri.TransformEnd()


# load mesh
troll=Obj.Obj("../meshes/troll.obj")

x=-10
y=-10

while (y<10) :
  while(x<10) :
    tx=Transformation()

    ri.TransformBegin()
    tx.setPosition(x,1.0,y)
    tx.setScale(0.7,random.uniform(0.6,0.8),0.7)
    tx.setRotation(0,random.uniform(0,360),0)
    ri.ConcatTransform(tx.getMatrix())
    baseColor=[random.uniform(0.2,1.0),random.uniform(0.2,1.0),random.uniform(0.2,1.0)]
    ri.Bxdf( "PxrDisney","bxdf", { 
                            "color baseColor" : baseColor, 
                            "float roughness" : [random.uniform(0.5,1.0)], 
                            "float clearcoat" : [random.uniform(0.2,1.0)], 
                            "float clearcoatGloss" : [random.uniform(0.4,1.0)]
                            })

    troll.SubDivisionMesh(ri)
    #ri.Sphere(1.0,-1,1,360)
    #print x,y
    x=x+0.6
    ri.TransformEnd()
  y=y+1.0
  x=-10

# floor
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1,1,1],
                        "float roughness" : [ 0.2 ],

                        })
s=12.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
