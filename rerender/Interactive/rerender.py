#!/usr/bin/python
import prman
import sys,time,os
sys.path.append('../../common')
from functions import drawTeapot,drawCube
from Camera import *

ri = prman.Ri() # create an instance of the RenderMan interface
# step one render scene to rib file
with open('scene.py','r') as scene :
    exec(scene)
print "rendered to Rib"
# now do re-render pass

ri.Begin('__render')

print "Pass 1"
ri.Display( "rerender", "it", "rgba")
ri.Hider('raytrace' ,
{
    'int incremental' :[1],
    "int minsamples"  : [1],
    "int maxsamples"  :[4] 
})

ri.PixelVariance(0)
ri.Integrator ("PxrPathTracer", "handle",
{ 
    "int maxPathLength" : [10] 
})	

ri.Option( "rerender", 
{
    "int[2] lodrange" : [0,3]
})
print "doing edits"
ri.EditWorldBegin( "bake.rib" , 
{
"string rerenderer" : "raytrace", 
"int progressive" : [1]
})

with open('edits.py','r') as edits :
    exec(edits)

fileTime = os.stat('edits.py').st_mtime
try :
    while True :
        currentFileTime = os.stat('edits.py').st_mtime  
        if  currentFileTime -fileTime > 0 :
            print "updating edit press CTRL + C to exit"
            fileTime = os.stat('edits.py').st_mtime
            with open('edits.py','r') as edits :
                exec(edits)

except KeyboardInterrupt:
    pass

ri.EditWorldEnd()
ri.End()

