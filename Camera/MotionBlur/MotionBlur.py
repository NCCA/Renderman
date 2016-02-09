#!/usr/bin/python

import sys
import math
import getpass
import time,random

# import the python renderman library
import prman

from vector import Vector
from Camera import *

# as the motion blur needs to interpolate each of the ri calls we need to block 
# them into seperate chunks

def Prop(rotation,Next) :
	ri.Rotate(90,0,0,1)
	# read in the nose cone data no need to blur
	ri.ReadArchive("Prop.rib")
	# this is our main interpolated rotation
	ri.MotionBegin([0,1])
	ri.Rotate(rotation,0,0,1)
	ri.Rotate(rotation+Next,0,0,1)
	ri.MotionEnd()
	# now we draw all the prop sections one at a time
	# note the transformbegin / end sections are outside the motion blocks
	# prop 1
	ri.TransformBegin()
	ri.MotionBegin([0,1])
	ri.Translate( 0 ,0.8, 0.4)
	ri.Translate( 0 ,0.8, 0.4)
	ri.MotionEnd()

	ri.MotionBegin([0,1])
	ri.Scale( 1 ,6 ,0.5)
	ri.Scale( 1 ,6 ,0.5)
	ri.MotionEnd()
	
	ri.MotionBegin([0,1])
	ri.Rotate( 10 ,0 ,1 ,0)
	ri.Rotate( 10 ,0 ,1 ,0)
	ri.MotionEnd()
	
	ri.MotionBegin([0,1])
	ri.Sphere( 0.15, -0.15, 0.15, 360)
	ri.Sphere( 0.15, -0.15, 0.15, 360)
	ri.MotionEnd()

	ri.TransformEnd()
	
	# prop 2
	
	
		# propellor 2	
	ri.TransformBegin()
	ri.MotionBegin([0,1])
	ri.Translate( 0 ,-0.8, 0.4)
	ri.Translate( 0 ,-0.8, 0.4)
	ri.MotionEnd()

	ri.MotionBegin([0,1])
	ri.Scale( 1 ,6 ,0.5)
	ri.Scale( 1 ,6 ,0.5)
	ri.MotionEnd()
	
	ri.MotionBegin([0,1])
	ri.Rotate( -10 ,0 ,1 ,0)
	ri.Rotate( -10 ,0 ,1 ,0)
	ri.MotionEnd()
	
	ri.MotionBegin([0,1])
	ri.Sphere( 0.15, -0.15, 0.15, 360)
	ri.Sphere( 0.15, -0.15, 0.15, 360)
	ri.MotionEnd()

	ri.TransformEnd()
	
	
	
ri = prman.Ri() # create an instance of the RenderMan interface
cam=Camera(Vector(-18,0.0,-28,1),Vector(0,0,0,1),Vector(0,1,0,0))
cam.fov=22
for frame in range(0,180) :
	filename = "MotionBlur.%03d.rib" %(frame) 
	
	ri.Begin(filename)
	ri.Option("rib", {"string asciistyle": "indented"})

	cam.Shutter(ri,0.0,1.0)
	
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("MotionBlur.%03d.exr"%(frame), "file", "rgba")
	
	cam.Format(ri)
	
	# now we start our world
	ri.WorldBegin()	
	cam.Place(ri)
	ri.TransformBegin()
	ri.ReadArchive("Lights.rib")
	ri.Color( [ 0.24, 0.24 ,0.3 ])
		
	Prop(frame*2,45)	
	
	ri.TransformEnd()
	ri.ReadArchive("aircraft.rib")
	# end our world
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
