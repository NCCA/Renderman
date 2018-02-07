#!/usr/bin/python
# import the python renderman library
import prman

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Primitives.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Primitives.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# now we start our world
ri.WorldBegin()

ri.Translate(0,0,10)
ri.TransformBegin()
ri.Translate(-4,2,0)
ri.Sphere(1,-1,1,360)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(-4,-2,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(1,-0.5,0.5,360) 
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(-1,2,0)
ri.Rotate(-90,1,0,0)
ri.Cone(2,1.0,360)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(-1,-2,0)
ri.Rotate(-90,1,0,0)
ri.Paraboloid(1.0,1.0,2.0,360)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(2,2,0)
ri.Rotate(-90,1,0,0)
ri.Hyperboloid([1.0,0.0,0.5],[1.0,0.0,-0.5],270)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(2,-2,0)
ri.Rotate(-90,1,0,0)
ri.Disk(0,1,360)
ri.TransformEnd()
ri.TransformBegin()
ri.Translate(3 ,0,0)
ri.Rotate(45,1,0,0)
ri.Torus(1.00,0.5,0,360,360)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
