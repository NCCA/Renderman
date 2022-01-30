#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
import getpass
import time

# import the python renderman library
import prman


def TorusWave(ri, nwaves, thetamax):
    if nwaves < 1:
        print("need positive number of waves")
        return
    innerrad = 2.0 / (8.0 * nwaves + 2)
    ri.Rotate(90.0, 1.0, 0.0, 0.0)
    ri.Sphere(innerrad, -innerrad, 0, thetamax)
    outerrad = 0.0
    for wave in range(1, nwaves):
        outerrad = outerrad + (innerrad * 2)
        ri.Torus(outerrad, innerrad, 0.0, 180.0, thetamax)
        outerrad = outerrad + (innerrad * 2)
        ri.Torus(outerrad, innerrad, 180.0, 360.0, thetamax)


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})
filename = "Archive.rib"
ri.Begin(filename)

# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, "File " + filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " + time.ctime(time.time()))

TorusWave(ri, 8, 360.0)
# and finally end the rib file
ri.End()
