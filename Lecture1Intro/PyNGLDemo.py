#!/usr/bin/env rmanpy3

import prman
from ncca.ngl import look_at, transformation

ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
ri.Begin("__render")

# FILENAME DISPLAY Type Output format
ri.Display("PyNGL.exr", "it", "rgba")
ri.Format(1024, 720, 1)
ri.Projection(ri.PERSPECTIVE)

# now we start our world
ri.WorldBegin()

ri.ArchiveRecord(ri.COMMENT, "move our world back 2 in the z so we can see it")
ri.Translate(0, 0, 2)
ri.ArchiveRecord(ri.COMMENT, "draw a sphere primitive")
ri.Sphere(1, -1, 1, 360)
# end our world
ri.ArchiveRecord(ri.COMMENT, "end our world")
ri.WorldEnd()
# and finally end the rib file
ri.End()
