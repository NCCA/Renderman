#!/usr/bin/python
import prman
# import the python functions
import sys,os.path,subprocess
import argparse
sys.path.append('../../common')
from functions import drawTeapot
import Obj
from Camera import Camera
from Vec4 import Vec4
from Transformation import *
import random

def main(filename,shadingrate=10,pixelvar=0.1,
         fov=48.0,width=1024,height=720,displace=1,
         integrator='PxrPathTracer',integratorParams={}
         
        ) :
  print 'shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams)
  ri = prman.Ri() # create an instance of the RenderMan interface

  # this is the begining of the rib archive generation we can only
  # make RI calls after this function else we get a core dump
  ri.Begin(filename)
  ri.Option('searchpath', {'string archive':'./assets/:../../meshes:@'})
  ri.Option('searchpath', {'string texture':'./textures/:../../meshes:@'})

  # now we add the display element using the usual elements
  # FILENAME DISPLAY Type Output format
  ri.Display('rgb.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  # setup the raytrace / integrators
  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })
 
  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})


  # Simple translate for our camera
  cam=Camera(Vec4(0,0.9,-2.9),Vec4(0,0.2,0),Vec4(0,1,0))
  cam.place(ri)


  # now we start our world
  ri.WorldBegin()

  #Lighting We need geo to emit light
  ri.TransformBegin()
  ri.AttributeBegin()

  ri.Declare('domeLight' ,'string')
  lightTx=Transformation()
  lightTx.setPosition(0,1,0)
  lightTx.setRotation(90,0,0)
  lightTx.setScale(1,1,1)
  ri.ConcatTransform(lightTx.getMatrix())

  ri.Light( 'PxrDomeLight', 'domeLight' ,{ 
                                          'float exposure' : [1.0],
                                          'string lightColorMap' : ['studio2.tx']
                                        })

  ri.AttributeEnd()
  ri.TransformEnd()

  # load mesh
  troll=Obj.Obj('../../meshes/troll.obj')
  ri.AttributeBegin()
  tx=Transformation()

  ri.Attribute ('trace' ,{'int displacements' : [ 1 ]})
  ri.Attribute ('displacementbound', {'float sphere' : [20], 'string coordinatesystem' : ['shader']})

  ri.Pattern('PxrTexture', 'TrollColour',{ 'string filename' : 'TrollColour.tx'})
  ri.Pattern('PxrTexture', 'TrollSpecular',{ 'string filename' : 'TrollSpec.tx'})


  ri.Pattern('PxrManifold2D' ,'texture_place',
  { 
    'string primvarS' : ['s'],
    'string primvarT' : ['t'],
    
  })
  ri.Pattern('PxrTexture', 'TrollNMap',
  { 
    'int invertT' : [0] , 
    'string filename' : '/Users/jmacey/teaching/Rendering/PixarExamples/scenes/displacement/lion_disp_zbrushTangent.tex',
    
    #'TrollNormal.tx',
    #'reference struct manifold' : ['texture_place:result']
  
  })

  # displacement is slow so if not doing it disable
  if displace == 1 :
    ## modes see  https://rmanwiki.pixar.com/display/REN/PxrDispTransform
    vectorSpace={'World' : 1 , 'Object' : 2 , 'Tangent' : 3, 'Current' : 4}
    displacementType={'Scalar' : 1, 'Vector' : 2 , 'Mudbox' : 3, 'Zbrush' : 4}
    remapMode={'None' : 1 , 'Centered' : 2 , 'Interpolate' : 3}
    dispSize=0.5
    
    ri.Pattern('PxrDispTransform','DispTransform',
    {
      'reference vector dispVector' : ['TrollNMap:resultRGB'],
      'uniform float dispDepth' : [dispSize],
      'uniform float dispHeight' : [dispSize],
      'uniform int dispType' : [displacementType.get('Zbrush')],  
      'uniform int vectorSpace' : [vectorSpace.get('Tangent')], 
      'uniform int dispRemapMode' : [remapMode.get('Centered')], 
      'uniform float dispCenter' : [0]
    })


    ri.Displace('PxrDisplace','zbrushDisplace' ,
    {   
      'reference vector dispVector' : ['DispTransform:resultXYZ'], 
      #'uniform float dispAmount' : [1.0],
      'int enabled' : [displace]
    })


  ri.Bxdf( 'PxrDisney','bxdf', 
  {  
    'reference color baseColor' : ['TrollColour:resultRGB'] ,  
    'reference color subsurfaceColor' : ['TrollColour:resultRGB'], 
    'float subsurface' : [0.4] , 
    'float metallic' : [0.1],
    'float specular' : [0.1],
    'float roughness' : [0.3]
  })
  '''
  ri.Bxdf( 'PxrDisney','bxdf', {  'color baseColor' : [0.8,0.8,0.8] })
  '''
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

  ri.AttributeEnd()


  # floor
  ri.TransformBegin()
  ri.AttributeBegin()
  ri.Bxdf( 'PxrDisney','bxdf', { 
                          'color baseColor' : [ 1,1,1],
                          'float roughness' : [ 0.2 ],

                          })
  #ri.Bxdf( 'PxrDiffuse','bxdf', {  'reference color diffuseColor' : ['colourChecker:resultRGB'] })
  ri.Displace('PxrDisplace','zbrushDisplace' ,
    {   
      'reference vector dispVector' : ['DispTransform:resultXYZ'], 
      #'uniform float dispAmount' : [1.0],
      'int enabled' : [displace]
    })

  ri.Pattern('PxrFractal','id',
  {
    'uniform float resultF' : [0.0],
    'uniform color resultRGB' : [1.0,1.0,1.0],
    'uniform int surfacePosition' : [0],
    'uniform int layers' : [0],
    'uniform float frequency' : [0.0],
    'uniform float lacunarity' : [0.0],
    'uniform float dimension' : [0.0],
    'uniform float erosion' : [0.0],
    'uniform float variation' : [0.0],
    'uniform int turbulent' : [0],
    'uniform point Q' : [0.0,0.0,0.0],
    'uniform float Qradius' : [0.0],
  })
  s=12.0
  face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
  ri.Patch('bilinear',{'P':face})
  ri.AttributeEnd()

  ri.TransformEnd()



  # end our world
  ri.WorldEnd()
  # and finally end the rib file
  ri.End()



def checkAndCompileShader(shader) :
  	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
		print 'compiling shader %s' %(shader)
		try :
			subprocess.check_call(['oslc', shader+'.osl'])
		except subprocess.CalledProcessError :
			sys.exit('shader compilation failed')
		 


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Modify render parameters')
  
  parser.add_argument('--shadingrate', '-s', nargs='?', 
                      const=10.0, default=10.0, type=float,
                      help='modify the shading rate default to 10')

  parser.add_argument('--pixelvar', '-p' ,nargs='?', 
                      const=0.1, default=0.1,type=float,
                      help='modify the pixel variance default  0.1')
  parser.add_argument('--fov', '-f' ,nargs='?', 
                      const=48.0, default=48.0,type=float,
                      help='projection fov default 48.0')
  parser.add_argument('--width' , '-wd' ,nargs='?', 
                      const=1024, default=1024,type=int,
                      help='width of image default 1024')
  parser.add_argument('--height', '-ht' ,nargs='?', 
                      const=720, default=720,type=int,
                      help='height of image default 720')
  parser.add_argument('--displace', '-ds' ,nargs='?', 
                      const=1, default=1,type=int,
                      help='enable displacement 0 off 1 on default on')
  
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


  main(filename,args.shadingrate,args.pixelvar,args.fov,args.width,args.height,args.displace,integrator,integratorParams)

