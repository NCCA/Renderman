## Introduction to Renderman

#### using the python api

---

## Introduction to Renderman

- When Renderman was first proposed it was a C like API for the development of scene descriptions to be rendered
- The description file produced is usually called a RIB (Renderman Interface Byte stream) file and this is then passed to the renderer
- The description of how the surface is to be textured and shaded is determined by a number of files called shaders

+++

## Modern Renderman (RIS)

- From Version 20 renderman introduced RIS

> RenderMan's RIS is a new rendering mode that is designed to be fast and easy to use while generating production-quality renders.

- There are a number of [sub-systems](https://renderman.pixar.com/resources/RenderMan_20/risOverview.html) 
  - Renderer, Camera, Integrator, Geometry, Materials, Patterns, Lights

+++

## Renderman Python
- As of Version 14 (2008) renderman has a python API
- It is similar to the C API and running a python script will output a rib file 
- Alternatively we can render directly from within the python script
- All of the notes presented will use the Python API to generate the rib files so we have the dual advantage of learning Python and prman at the same time.

+++

## Renderman Pipeline

<img src="slides/lecture1/images/pipeline.png" width="50%">


---?code=Lecture1Intro/HelloWorld.rib&lang=C

-  A rib file is a simple text file, using an editor, type in the following

