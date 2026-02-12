#!/usr/bin/env -S uv run --script

import prman
from RendermanContext import AttributeBegin, Begin, FrameBegin, MotionBegin, ObjectBegin, TransformBegin, WorldBegin, ri

if __name__ == "__main__":
    ri.Option("rib", {"string asciistyle": "indented"})
    with Begin("__render"):
        with FrameBegin(1):
            ri.Display("TestContext.exr", "it", "rgba")
            ri.Format(720, 576, 1)
            ri.Projection(ri.PERSPECTIVE)
            ri.Translate(0, 0, 2)
            ri.Shutter(0, 1)
            with WorldBegin():
                with ObjectBegin() as id:
                    with TransformBegin():
                        ri.Translate(0, 0, 0)
                        ri.Scale(0.1, 0.1, 0.1)
                        ri.Rotate(-90, 1, 0, 0)
                        with MotionBegin([0, 1]):
                            ri.Translate(-0.2, 0, 0)
                            ri.Translate(0.2, 0, 0)
                        ri.Geometry("teapot")

                with TransformBegin(), AttributeBegin():
                    ri.Scale(0.1, 0.1, 0.1)
                    ri.Translate(-1, 0, 0)
                    ri.Sphere(1, -1, 1, 360)
                with AttributeBegin(), TransformBegin():
                    ri.Translate(1, 0, 0)
                    ri.ObjectInstance(id)
