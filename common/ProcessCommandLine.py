import argparse

filename='default.rib'
integratorParams={"int numLightSamples" : [1], "int numBxdfSamples" : [1], "int maxPathLength" : [4]}
integrator='PxrPathTracer'
args=[]

def ProcessCommandLine(_filename) :
  global filename
  global integratorParams
  global integrator
  global args
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
  
  parser.add_argument('--rib', '-r' , action='count',help='render to rib not framebuffer')
  parser.add_argument('--default', '-d' , action='count',help='use PxrPathTracer')
  parser.add_argument('--vcm', '-v' , action='count',help='use PxrVCM')
  parser.add_argument('--unified', '-i' , action='count',help='use PxrUnified')
  parser.add_argument('--occlusion', '-o' , action='count',help='use Occlusion')
  
  parser.add_argument('--direct', '-t' , action='count',help='use PxrDirect')
  parser.add_argument('--wire', '-w' , action='count',help='use PxrVisualizer with wireframe shaded')
  parser.add_argument('--normals', '-n' , action='count',help='use PxrVisualizer with wireframe and Normals')
  parser.add_argument('--st', '-u' , action='count',help='use PxrVisualizer with wireframe and ST')

  args = parser.parse_args()
  if args.rib :
    filename = _filename 
  else :
    filename='__render'
  
  if args.default :
    integrator='PxrPathTracer'
  if args.vcm :
    integrator='PxrVCM'
  if args.unified :
    integrator='PxrUnified'
  if args.occlusion :
    integrator='PxrOcclusion'
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

