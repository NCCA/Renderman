#!/usr/bin/python
from __future__ import print_function
import sys
sys.path.append('../common')
import prman,os,Transformation
import ProcessCommandLine as cl
# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,
         fov=48.0,width=1024,height=720,
         integrator='PxrPathTracer',integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
  ri = prman.Ri() # create an instance of the RenderMan interface

  # this is the begining of the rib archive generation we can only
  # make RI calls after this function else we get a core dump
  ri.Begin(filename)
  ri.Option('searchpath', {'string archive':'./assets/:@'})
  ri.Option('searchpath', {'string texture':'./textures/:@'})

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

  ri.Rotate(12,1,0,0)
  ri.Translate( 0, 0.75 ,2.5)


  # now we start our world
  ri.WorldBegin()
  #######################################################################
  #Lighting We need geo to emit light
  #######################################################################
  ri.TransformBegin()
  ri.AttributeBegin()
  ri.Declare('domeLight' ,'string')
  ri.Rotate(-90,1,0,0)
  ri.Rotate(100,0,0,1)
  ri.Attribute( 'visibility' ,{ 'int indirect' : [0], 'int transmission' : [0] ,'int camera' : [0]})
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'Luxo-Jr_4000x2000.tex'
   })
   
  ri.AttributeEnd()
  ri.TransformEnd()

  ri.TransformBegin()
  ri.AttributeBegin()
  ri.Attribute( 'visibility' ,{ 'int indirect' : [0], 'int transmission' : [0] ,'int camera' : [1]})
  ri.Declare('Light0' ,'string')
  tx=Transformation.Transformation()
  tx.setPosition(-0.9,0.9,0.5)
  tx.setRotation(90,60,35)
  ri.Identity()
  ri.Transform(tx.getMatrix())
  ri.Light( 'PxrRectLight', 'Light0', { 'float intensity' : 4})


  tx.setPosition(0.9,0.9,0.5)
  tx.setRotation(90,60,-35)
  tx.setScale(0.2,0.2,0.2)
  ri.Identity()
  ri.Transform(tx.getMatrix())
  ri.Light( 'PxrRectLight', 'Light0', { 'float intensity' : 2})


  ri.AttributeEnd()
  ri.TransformEnd()
  #######################################################################
  # end lighting
  #######################################################################

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'floor'})
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.8,0.8,0.8]
  })
  ri.Polygon( {ri.P: [-1, -1 ,1 ,1, -1, 1, 1, -1, -2, -1, -1, -2]})
  ri.AttributeEnd()

  ri.AttributeBegin()
  HairColour={'Blond' : [0.921, 0.898, 0.321], 
              'Blue' : [0.1, 0.1, 0.8]}
  ri.Bxdf('PxrMarschnerHair','id',
  {
  'int diffuseModelType' : [0], 
  'float diffuseGain' : [0.3], 
  'color diffuseColor' : HairColour.get('Blue'), 
  'float specularGainR' : [1.0], 
  'float specularGainTRT' : [1.0], 
  'float specularGainTT' : [1.0], 
  'float specularGainGLINTS' : [1.0], 
  'color specularColorR' : [1.0,1.0,1.0], 
  'color specularColorTRT' : HairColour.get('Blue'), 
  'color specularColorTT' : [0.5,0.2,0.3], 
  'float specularConeAngleR' : [8.0], 
  'float specularConeAngleTRT' : [8.0], 
  'float specularConeAngleTT' : [8.0], 
  'float specularOffset' : [-3], 
  'float specularIor' : [1.55], 
  'float specularMixFresnel' : [1.0], 
  'float specularGlintWidth' : [10.0], 
  'float specularEccentricity' : [1.0], 
  'float glowGain' : [0.0], 
  'color glowColor' : [1,1,1], 
  'float specularEnergyCompensation' : [0.0], 
  'normal eccentricityDirection' : [0,0,0], 
  'color shadowColor' : [0.0,0.0,0.0], 
  'float presence' : [1.0], 
  'int inputAOV' : [0], 
  })
  ri.Translate(0,-0.2,-1)
  ri.Rotate(90,0,1,0)
  ri.Scale(0.1,0.1,0.1)
  ri.ReadArchive('hair.rib')
  ri.AttributeEnd()



  # end our world
  ri.WorldEnd()
  # and finally end the rib file
  ri.End()



def checkAndCompileShader(shader) :
  	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
		print( 'compiling shader %s' %(shader))
		try :
			subprocess.check_call(['oslc', shader+'.osl'])
		except subprocess.CalledProcessError :
			sys.exit('shader compilation failed')
		 


if __name__ == '__main__':
  shaderName='starBall'
  checkAndCompileShader(shaderName)
  
  cl.ProcessCommandLine('Hair.rib')
  main(cl.filename,cl.args.shadingrate,cl.args.pixelvar,cl.args.fov,cl.args.width,cl.args.height,cl.integrator,cl.integratorParams)

