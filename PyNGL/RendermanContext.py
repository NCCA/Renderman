#!/usr/bin/env rmanpy3
"""A set of context managers for simplifying RenderMan RIB generation."""

from contextlib import contextmanager
from typing import Generator, List

import prman

"""
Global renderman context must be imported into other modules.
"""
ri: prman.Ri = prman.Ri()


@contextmanager
def WorldBegin() -> Generator[None, None, None]:
    """A context manager for a WorldBegin/WorldEnd block."""
    ri.WorldBegin()
    yield
    ri.WorldEnd()


@contextmanager
def AttributeBegin() -> Generator[None, None, None]:
    """A context manager for an AttributeBegin/AttributeEnd block."""
    ri.AttributeBegin()
    yield
    ri.AttributeEnd()


@contextmanager
def TransformBegin() -> Generator[None, None, None]:
    """A context manager for a TransformBegin/TransformEnd block."""
    ri.TransformBegin()
    yield
    ri.TransformEnd()


@contextmanager
def Begin(filename: str) -> Generator[None, None, None]:
    """A context manager for a Begin/End block to start a RIB file.

    Args:
        filename: The name of the RIB file to create.
    """
    ri.Begin(filename)
    yield
    ri.End()


@contextmanager
def FrameBegin(frame: int) -> Generator[None, None, None]:
    """A context manager for a FrameBegin/FrameEnd block.

    Args:
        frame: The frame number to render.
    """
    ri.FrameBegin(frame)
    yield
    ri.FrameEnd()


@contextmanager
def ObjectBegin() -> Generator[int, None, None]:
    """A context manager for an ObjectBegin/ObjectEnd block.

    Yields:
        The object ID.
    """
    id = ri.ObjectBegin()
    yield id
    ri.ObjectEnd()


@contextmanager
def MotionBegin(num_keys: List[float]) -> Generator[None, None, None]:
    """A context manager for a MotionBegin/MotionEnd block.

    Args:
        num_keys: A list of motion times.
    """
    ri.MotionBegin(num_keys)
    yield
    ri.MotionEnd()


if __name__ == "__main__":
    ri.Option("rib", {"string asciistyle": "indented"})
    with Begin("__render"):
        with FrameBegin(1):
            ri.Display("test.exr", "it", "rgba")
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

__all__ = ["WorldBegin", "AttributeBegin", "TransformBegin", "Begin", "FrameBegin", "ObjectBegin", "MotionBegin", "ri"]
