#!/usr/bin/python
import prman
# import the python functions
import sys
sys.path.append('../common')
from functions import drawTeapot
import Obj
from Camera import Camera
from Vec4 import Vec4




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
cam=Camera(Vec4(2,2,2),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)


# now we start our world
ri.WorldBegin()
#Lighting We need geo to emit light
ri.TransformBegin()
ri.AttributeBegin()

ri.Translate(0,1,0)
ri.Rotate(-45,1,0,0)
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight", "float exposure"  : [2],
                                       })
ri.Scale(.1,.2,.1)
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color emitColor" : [ 1,1,1]
                        })

#ri.Geometry("rectlight")
ri.Sphere(1.0,-1,1,360)
ri.AttributeEnd()
ri.TransformEnd()





# first teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float metallic" : [ 0 ]
                        })
drawTeapot(ri,x=-1)

# troll
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float metallic" : [ 0.6 ]
                        })

ri.Rotate(180,0,1,0)
ri.Scale(0.7,0.7,0.7)
ri.Translate(0,0.6,0)                        
troll=Obj.Obj("troll.obj")
troll.SubDivisionMesh(ri)
ri.TransformEnd()
# third teapot
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 0.8, 0.2, 0.2], 
                        "float roughness" : [ 0.5 ],
                        "float metallic" : [ 1.0 ]
                        })
drawTeapot(ri,x=1)
# floor
ri.TransformBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                        "color baseColor" : [ 1,1,1],
                        "float roughness" : [ 0.2 ],
                        "float metallic" : [ 0.8 ]

                        })
s=2.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch("bilinear",{'P':face})

ri.TransformEnd()



# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
