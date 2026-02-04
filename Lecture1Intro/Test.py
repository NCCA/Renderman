#!/usr/bin/env rmanpy3
import prman

ri = prman.Ri()  #

ri.Begin("__render")

ri.Display("Test.exr", "framebuffer", "rgba")
ri.WorldBegin()
ri.Translate(0, 0, 3)
ri.Geometry("teapot")
ri.WorldEnd()
ri.End()
