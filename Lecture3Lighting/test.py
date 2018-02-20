#!/usr/bin/python
import prman
# import the python functions
import sys

import argparse

# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,integrator='PxrPathTracer',integratorParams={}) :
  print "shading rate {} pivel variance {} using {} {}".format(shadingrate,pixelvar,integrator,integratorParams)
  ri = prman.Ri() # create an instance of the RenderMan interface

  # this is the begining of the rib archive generation we can only
  # make RI calls after this function else we get a core dump
  ri.Begin(filename)
  ri.Option('searchpath', {'string archive':'./assets/:@'})

  # now we add the display element using the usual elements
  # FILENAME DISPLAY Type Output format
  ri.Display('rgb.exr', 'it', 'rgba')
  ri.Format(1024,720,1)

  # setup the raytrace / integrators
  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })
  '''
  ri.Projection ('PxrCamera' , 
  { 'fov' : 45,
  # 'float tilt' : 7.5,
    'float radial1' : -0.1,
  #  'color axial' : [-0.02, 0 ,0.02] ,
  #  'color transverse' : [0.98 ,1 ,1.02],
    'float natural' : 1.0 ,
    'float optical' : 1.0,
  # 'float shiftY' : 0.5,
  # 'string sweep' : 'down',
  # 'float duration' : 0.1
    })
  #ri.DepthOfField( 3 ,1 ,5)
  '''

  ri.Projection(ri.PERSPECTIVE,{ri.FOV:50})

  ri.Rotate(15,1,0,0)
  ri.Translate( 0, 0.8 ,2.1)


  # now we start our world
  ri.WorldBegin()
  #######################################################################
  #Lighting We need geo to emit light
  #######################################################################
  ri.TransformBegin()
  ri.AttributeBegin()
  ri.Declare('meshLight' ,'string')
  ri.Light( 'PxrMeshLight', 'meshLight', { 'float intensity' : 30})
  ri.ShadingRate(1)
  ri.Sides(1)
  ri.Patch( 'bilinear',
  {
    'P'  :[-0.25, 0.99, -0.25, 0.25, 0.99, -0.25, -0.25, 0.99, 0.25, 0.25, 0.99, 0.25]
  })
  ri.AttributeEnd()
  ri.TransformEnd()
  #######################################################################
  # end lighting
  #######################################################################

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'cornell'})
  ri.ReadArchive('cornell.rib')
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'buddha'})
  ri.TransformBegin()
  ri.Translate(-0.5,-1,0)
  ri.Rotate(180,0,1,0)
  ri.Scale(0.1,0.1,0.1)
  ri.ReadArchive('buddha.zip!buddha.rib')
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'sphere'})
  ri.TransformBegin()
  ri.Translate(0.3, -0.7 , 0.3)
  ri.Sphere(0.3,-0.3,0.3,360)
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'teapot'})
  ri.TransformBegin()
  ri.Translate(0, -1 , -0.8)
  ri.Rotate(45,0,1,0)
  ri.Rotate( -90, 1 ,0 ,0)
  ri.Scale( 0.1, 0.1, 0.1) 
  ri.Geometry('teapot')
  ri.TransformEnd()
  ri.AttributeEnd()

  # end our world
  ri.WorldEnd()
  # and finally end the rib file
  ri.End()

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description='Modify render parameters')
  
  parser.add_argument('--shadingrate', '-s', nargs='?', 
                      const=10.0, default=10.0, type=float,
                      help='modify the shading rate default to 10')

  parser.add_argument('--pixelvar', '-p' ,nargs='?', 
                      const=0.1, default=0.1,type=float,
                      help='modify the pixel variance default  0.1')
  
  parser.add_argument('--rib', '-r' , action='count',help='render to rib not framebuffer')
  parser.add_argument('--default', '-d' , action='count',help='use PxrDefault')
  parser.add_argument('--vcm', '-v' , action='count',help='use PxrVCM')
  parser.add_argument('--direct', '-t' , action='count',help='use PxrDirect')
  parser.add_argument('--wire', '-w' , action='count',help='use PxrVisualizer with wireframe shaded')
  parser.add_argument('--normals', '-n' , action='count',help='use PxrVisualizer with wireframe and Normals')
  parser.add_argument('--st', '-u' , action='count',help='use PxrVisualizer with wireframe and ST')

  args = parser.parse_args()
  if args.rib :
    filename = 'rgb.rib' 
  else :
    filename='__render'
  
  integratorParams={}
  integrator='PxrPathTracer'
  if args.default :
    integrator='PxrDefault'
  if args.vcm :
    integrator='PxrVCM'
  if args.direct :
    integrator='PxrDirectLighting'
  if args.wire :
    integrator='PxrVisualizer'
    integratorParams={'int wireframe' : [1], 'string style' : ['shaded']}
  if args.normals :
    integrator='PxrVisualizer'
    integratorParams={'int wireframe' : [1], 'string style' : ['normals']}
  if args.st :
    integrator='PxrVisualizer'
    integratorParams={'int wireframe' : [1], 'string style' : ['st']}


  main(filename,args.shadingrate,args.pixelvar,integrator,integratorParams)

