#!/usr/bin/python
from __future__ import print_function
import prman
import ProcessCommandLine as cl
# import the python functions
import sys,os.path,subprocess
sys.path.append('../common/')
import Mat4
# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,
         fov=48.0,width=1024,height=720,
         integrator='PxrPathTracer',integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
  ri = prman.Ri() # create an instance of the RenderMan interface

  ri.Option("rib", {"string asciistyle": "indented,wide"})
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
  ri.Translate( 0, 0.75 ,6.5)


  # now we start our world
  ri.WorldBegin()
  #######################################################################
  #Lighting 
  #######################################################################
  
  ri.AttributeBegin()
  # position x,y,z rot [axis x,y,z]
  xpos=1.0
  positions=[[-xpos,-0.2,0,90,0,1,0],[xpos,-0.2,0,-90,0,1,0],[-xpos,-0.2,-1,90,0,1,0],[xpos,-0.2,-1,-90,0,1,0],[-xpos,-0.2,-2,90,0,1,0],[xpos,-0.2,-2,-90,0,1,0],[-xpos,-0.2,-3,90,0,1,0],[xpos,-0.2,-3,-90,0,1,0],[-xpos,-0.2,-4,90,0,1,0],[xpos,-0.2,-4,-90,0,1,0],[-xpos,-0.2,-5,90,0,1,0],[xpos,-0.2,-5,-90,0,1,0],[0,-0.2,0.8,180,0,1,0],
  [0,2,0,0,0,1,0],[0,0.8,-1,90,1,0,0],[0,0.8,-2,90,1,0,0],[0,0.8,-3,90,1,0,0],[0,0.8,-4,90,1,0,0]]
  lightNum=0
  ri.Attribute( 'visibility' ,{ 'int indirect' : [0], 'int transmission' : [0] ,'int camera' : [1]})
  # rotation matrix for the master image used in portals
  xrot=Mat4.Mat4()
  xrot.rotateX(90)
  yrot=Mat4.Mat4()
  yrot.rotateY(180)
  tx=yrot*xrot

  for p in positions :
    ri.TransformBegin()    
    ri.Declare('portalLight{0}'.format(lightNum) ,'string')
    ri.Translate(p[0],p[1],p[2])
    ri.Rotate(p[3],p[4],p[5],p[6])
    ri.Scale(0.5,0.5,1)
    lightNum=lightNum+1
    ri.Light( 'PxrPortalLight', 'portalLight', { 
              'float exposure' : 1.0,
              'float intensity' : 1.0,
              'string domeColorMap' : ['Luxo-Jr_4000x2000.tex'],
              'matrix portalToDome' : tx.getMatrix(),             
    })
    ri.TransformEnd()
  ri.AttributeEnd()

  #######################################################################
  # end lighting
  #######################################################################

  ri.AttributeBegin()
  ri.TransformBegin()
  ri.Attribute( 'identifier',{ 'name' :'cornell'})
  ri.Scale(1.0,1.0,1.5)
  ri.ReadArchive('cornell.rib')
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'buddha'})
  ri.TransformBegin()
  ri.Translate(-0.5,-1,-4)
  ri.Rotate(180,0,1,0)
  ri.Scale(0.1,0.1,0.1)
  ri.Attribute( 'visibility',{ 'int transmission' : [1]})
  ri.Attribute( 'trace',
  { 
    'int maxdiffusedepth' : [1], 
    'int maxspeculardepth' : [8]
  })
  ri.Bxdf('PxrSurface', 'greenglass',{ 
  'color refractionColor' : [0,0.9,0],
  'float diffuseGain' : 0,
  'color specularEdgeColor' : [0.2, 1 ,0.2],
  'float refractionGain' : [1.0],
  'float reflectionGain' : [1.0],
  'float glassRoughness' : [0.01],
  'float glassIor' : [1.5],
  'color extinction' : [0.0, 0.2 ,0.0],
  
  })

  ri.ReadArchive('buddha.zip!buddha.rib')
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'sphere'})
  ri.Pattern('PxrVariable','du', {'string variable': 'du', 'string type' : 'float'})
  ri.Pattern('PxrVariable','dv', {'string variable': 'dv', 'string type' : 'float'})
  ri.Pattern('starBall','starBall', { 
            'reference float du' : ['du:resultR'], 
            'reference float dv' : ['dv:resultR']
            })

  ri.Bxdf( 'PxrDisney','bxdf', { 'reference color baseColor' : ['starBall:Cout'] })
  ri.TransformBegin()
  ri.Translate(0.3, -0.7 , -4.3)
  ri.Rotate(-30,0,1,0)
  ri.Rotate(20,1,0,0)
  ri.Sphere(0.3,-0.3,0.3,360)
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'teapot'})
  ri.TransformBegin()
  ri.Translate(0, -1 , -4.8)
  ri.Rotate(45,0,1,0)
  ri.Rotate( -90, 1 ,0 ,0)
  ri.Scale( 0.1, 0.1, 0.1) 
  ri.Bxdf('PxrSurface', 'plastic',{
          'color diffuseColor' : [.04, .51, .1],
          'color clearcoatFaceColor' : [.5, .5, .5], 
          'color clearcoatEdgeColor' : [.25, .25, .25]
  })
  ri.Geometry('teapot')
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Bxdf('PxrSurface', 'metal', {
          'float diffuseGain' : [0],
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [1 ,1 ,1],
          'color specularIor' : [4.3696842, 2.916713, 1.654698],
          'color specularExtinctionCoeff' : [5.20643, 4.2313662, 3.7549689],
          'float specularRoughness' : [0.1], 
          'integer specularModelType' : [1] 
  })

  ri.Attribute('identifier',{ 'name' :'ncca'})
  ri.TransformBegin()
  ri.Translate(0, 0.3 , 0.8)
  ri.ReadArchive('ncca.rib')
  ri.TransformEnd()
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
  
  cl.ProcessCommandLine('portalRoom.rib')
  main(cl.filename,cl.args.shadingrate,cl.args.pixelvar,cl.args.fov,cl.args.width,cl.args.height,cl.integrator,cl.integratorParams)

