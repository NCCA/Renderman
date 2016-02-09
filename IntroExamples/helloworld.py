#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import getpass
import time
# import the python renderman library
import prman

ri = prman.Ri() # create an instance of the RenderMan interface

filename = "__render" #"HelloWorld.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('test.rib')
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'Comments start with a #')
ri.ArchiveRecord(ri.COMMENT, 'File HelloWorld.rib #')
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("HelloWorld.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE)

# now we start our world
ri.WorldBegin()
# move back 2 in the z so we can see what we are rendering
ri.ArchiveRecord(ri.COMMENT, 'move our world back 2 in the z so we can see it')
ri.Translate(0,0,2)
ri.ArchiveRecord(ri.COMMENT, 'draw a sphere primitive')
ri.Sphere (1,-1, 1, 360)
# end our world
ri.ArchiveRecord(ri.COMMENT, 'end our world')
ri.WorldEnd()
# and finally end the rib file
ri.End()
