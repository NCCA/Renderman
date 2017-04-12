#!/usr/bin/python
import prman


def drawTeapot(ri,x=0,y=0,z=0,rx=-90.0,ry=45.0,rz=0.0,sx=0.2,sy=0.2,sz=0.2) :
  ri.TransformBegin()
  ri.Translate(x,y,z)
  ri.Rotate(ry,0,1,0)
  ri.Rotate( rx, 1 ,0 ,0)
  ri.Scale( sx, sy, sz) 
  ri.Geometry( "teapot")
  ri.TransformEnd()  

