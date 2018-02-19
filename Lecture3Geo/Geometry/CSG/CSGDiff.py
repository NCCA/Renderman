#!/usr/bin/python
import prman

def Scene(ri) :
	ri.SolidBegin('difference')   
	ri.SolidBegin('primitive')
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Translate( 0,-1.0,0)
	ri.Rotate(-90,1,0,0)
	ri.Rotate(36,0,0,1)
	ri.Scale(0.4,0.4,0.4)
	ri.Geometry('teapot')
	ri.AttributeEnd()
	ri.TransformEnd()
	ri.SolidEnd()

	for i in range(0,360,20) :
		ri.SolidBegin('primitive')
		ri.Rotate(i,0,1,0)	
		ri.Translate(-0.6,-0.3,0)
		ri.Scale(0.3,0.2,0.3)
		ri.Sphere(1,-1,1,360)
		ri.SolidEnd()
	ri.SolidEnd()
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option('rib', {'string asciistyle': 'indented'})

filename = 'CSGDifference.rib'
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('CSGDifference.exr', 'it', 'rgba')
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
ri.Hider("raytrace" ,{"int incremental" :[1]})
ri.PixelVariance (0.02)
ri.ShadingRate(20)
ri.Integrator ("PxrPathTracer" ,"integrator")
# now we start our world
ri.WorldBegin()
#######################################################################
#Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
# position light
ri.Translate(0.0,1.5,3)
ri.Rotate(180,1,0,0)
ri.Rotate(-30,1,0,0)
# add geometry for debug (off screen here)
ri.Bxdf( "PxrDisney","bxdf", {"color emitColor" : [ 1,1,1] })
ri.Geometry("rectlight")
# enable light
ri.Light( 'PxrRectLight', 'areaLight',{'float exposure' : [3] })
ri.AttributeEnd()
ri.TransformEnd()


ri.Translate(-0.2,0.2,2)
ri.TransformBegin()
#ri.Rotate(-90,1,0,0)
ri.Bxdf( 'PxrDisney','bxdf', 
{ 
	'color baseColor' : [ 1.0, 0.0, 0.0], 
})
Scene(ri)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()
