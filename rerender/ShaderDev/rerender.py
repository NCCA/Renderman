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
ri.Display( "rerender", "it", "rgba")
ri.Hider('raytrace' ,
{
    'int incremental' :[1],
    "int minsamples"  : [1],
    "int maxsamples"  :[4] 
})

ri.PixelVariance(10)
ri.Integrator ("PxrPathTracer", "handle",
{ 
    "int maxPathLength" : [10] 
})	

ri.Option( "rerender", 
{
    "int[2] lodrange" : [0,3]
})
print "Baking Scene for re-render"
ri.EditWorldBegin( "bake.rib" , 
{
"string rerenderer" : "raytrace", 
"int progressive" : [1]
})

# do a null edit to get the scene to display
ri.EditBegin('null')
ri.EditEnd()
print 'Modify and save edits.py to update scene'
# grab the current time of the edits.py file
fileTime = os.stat('edits.py').st_mtime
# now loop until we get a CTR+C press
try :
    while True :
        # stat the file and see if it has changed
        currentFileTime = os.stat('edits.py').st_mtime  
        if  currentFileTime -fileTime > 0 :
            print "updating edit press CTRL + C to exit"
            with open('edits.py','r') as edits :
                exec(edits)
            fileTime = os.stat('edits.py').st_mtime

except KeyboardInterrupt:
    pass

ri.EditWorldEnd()
ri.End()

