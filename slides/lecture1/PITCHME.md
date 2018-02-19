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

---?code=Lecture1Intro/HelloWorld.rib&lang=C&title=[HelloWorld.rib](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/HelloWorld.rib)

@[1-13](A rib file is a simple text file, using an editor, type in the following)
@[1-2](# used for comments)
@[3](specify the version of the RI specification used)
@[4](Specify the display driver, in this case the simple framebuffer one with an RGBA output)
@[5](What size image and pixel ratio to produce)
@[6](What type of projection to use)
@[7,13](Everything within the world will be rendered)
@[8,9](Translate back 2 in the Z)
@[10,11](Draw a Sphere)

+++

## Rendering the file
- To render the file use the following command line

```bash
render -t:2 HelloWorld.rib
```

- In the example we use the default ```"framebuffer"``` display driver which will use the ```sho``` program.
- If we wish to use the more powerful Image Tool (it) we can change the drive, however it must be running first.

+++

## Render to file
- Typically we will render to a file on disk to do this we can specify the ```file``` driver

```
Display "Diffuse.exr" "file" "rgba"
```

- Output file name will be inferred from the filename
- Extra files / channels can be added using the + prefix

```
Display "+Normal.exr" "file" "N"
```

---

## Python Version

- The python script to generate the rib file is a lot larger as we need to do some initial setup for the interface
- All rib commands belong to the namespace ri and are prefixed with ri
- Apart from that the function names are the same as the raw rib commands
- The following file was used to create the HelloWorld rib file

+++?code=Lecture1Intro/helloworld.py&lang=python&title=helloworld.py
@[1-37](ensure the correct python path is set)
@[6-13](We create an instance of the RI interface to use)
@[14-15](This allows us to write to the rib stream)
@[20-37](Python functions are analogous to the basic RIB commands)

+++

## ```'__render'```

- the keyword ```'__render'``` passed to the ```ri.Begin()``` function will cause the rib file to be passed to the renderer
- in most cases this is a very quick way of rendering a scene to either file or framebuffer
- however in some cases this will not work properly (especially with procedurals)

---

#### Cameras and Transformations
- by default the current transformation matrix contains the identity matrix as the screen transformation. 
- Usually the first transformation command is an RiProjection, which appends the projection matrix onto the screen transformation, saves it, and reinitializes the current transformation matrix as the identity camera transformation. 

+++

#### Cameras and Transformations

- After the camera coordinate system is established, future transformations move the world coordinate system relative to the camera coordinate system. 
- When an RiWorldBegin is executed, the current transformation matrix is saved as the camera transformation, and thus the world coordinate system is established. 
- Subsequent transformations inside of an RiWorldBegin- RiWorldEnd establish different object coordinate systems.

+++

#### Camera to Raster projection geometry
<img src="slides/lecture1/images/camera1.png" width="50%">

+++

### Camera Positioning

```C
RiBegin ();
  RiFormat ( xres, yres, 1.0 );  // Raster coordinate system 
  RiFrameAspectRatio ( 4.0/3.0 );  // Screen coordinate system
  RiFrameBegin (0);
    RiProjection ("perspective,"...); // Camera coordinate system
    RiRotate (... );
    RiWorldBegin (); // World coordinate system
      ...
      RiTransform (...);  // Object coordinate system
    RiWorldEnd ();
  RiFrameEnd (); 
RiEnd ();
```

---


## Transformations

- Transformations are used to transform points between coordinate systems. 
- At various points when defining a scene the current transformation is used to define a particular coordinate system. 
  - RiProjection establishes the camera coordinate system
  - RiWorldBegin establishes the world coordinate system.

+++

## Current Transformation

- The current transformation is maintained as part of the graphics state. 
- Issuing transform commands will concatenate that transformation onto the current transformation. 
- These include the basic linear transformations 
  - translation, rotation, skew, scale and perspective. 
- This is done using a 4x4 Transform Matrix 

+++

## Moving Things Around
- In the first example the command Translate is used to move the object 2 in the Z.
- Renderman treats +ve Z as going into the screen (opposite to OpenGL)
- Renderman (and ribs) work with a Fixed Camera and the world must be moved to be in the correct position for the fixed camera
- This can be counter intuitive at first but you soon get used to it.

+++

## Grouping Transforms
- To group transforms we use the ```TransformBegin``` and ```TransformEnd``` commands
- These are similar to the OpenGL ```glPushMatrix()``` and ```glPopMatrix()``` and preserve the current transformation state


+++?code=Lecture1Intro/transform1.py&lang=python&title=[transform1.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/transform1.py)

+++

### [transform1.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/transform1.py)

<img src="slides/lecture1/images/transform1.png" width="50%">

- Note how the cumulative transforms work in this example

+++?code=Lecture1Intro/transform2.py&lang=python&title=[transform2.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/transform2.py)

+++
### [transform2.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/transform2.py)

<img src="slides/lecture1/images/transform2.png" width="50%">

- ```TransformBegin / End``` block resets the transform

+++

## Other Affine Transforms

- Scale x y z : scales the current active elements in x y and z
- Rotate [angle] x y z : rotate around the axis by [angle] degrees
- Identity : restores the transformation matrix to what is was before world begin

```
# scale around the origin x,y,z
ri.Scale(1,2,1)

#rotate -90 degrees around the vector [1 0 0] (x)
ri.Rotate(-90,1,0,0)

# set the transform to the identity matrix
ri.Identity()
```

---

## Quadrics
- Many common shapes can be modelled with quadrics.
- All the following quadrics are rotationally symmetric about the z axis. 
- In all the quadrics u and v are assumed to run from 0 to 1. 

```
Sphere radius zmin zmax sweepangle
Cylinder radius zmin zmax sweepangle
Cone height radius sweepangle
Paraboloid topradius zmin zmax sweepangle
Hyperboloid point1 point2 sweepangle
Disk height radius sweepangle
Torus majorrad minorrad phimin phimax sweepangle
```

+++

## Quadrics

<img src="slides/lecture1/images/quad1.png" width="50%">


+++

## Quadrics

<img src="slides/lecture1/images/quad2.png" width="50%">

+++?code=Lecture1Intro/Primitives.py&lang=python&title=[Primitives.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/Primitives.py)

+++

## [Primitives.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/Primitives.py)

<img src="slides/lecture1/images/Primitives.png" width="50%">


---

## What No Cube?

- Renderman uses patches and we can combine them to make a cube.
```
Patch “type” [parameterlist]
```

- Define a single patch. type can be either "bilinear" or "bicubic". parameterlist is a list of token-array pairs where each token is one of the standard geometric primitive variables 

+++

## Parameter Lists


| Name	| Declared Type	| Description |
|-------|---------------|-------------|
|```"P"```	| ```vertex point```	| Position | 
|```"Pw"```	| ```vertex hpoint```	| Position in homogeneous cords | 
|```"N"```	| ```varying Normal```	| Phong shading normals | 

+++

## Parameter Lists

| Name	| Declared Type	| Description |
|-------|---------------|-------------|
|```"Cs"```	| ```varying colour```	| Surface Colour (access in Shader?) | 
|```"Os"```	| ```varying colour```	| Surface opacity (access in Shader?) | 
|```"st"```	| ```varying float[2]```	| Texture Co-ordinates | 

+++

## Patches

- Four points define a bilinear patch, and 16 define a bicubic patch. - The order of vertices for a bilinear patch is (0,0),(1,0),(0,1),(1,1). 
- Note that the order of points defining a quadrilateral is different depending on whether it is a bilinear patch or a polygon. 
- The vertices of a polygon would normally be in clockwise (0,0),(0,1),(1,1),(1,0) order.

+++

## Instance Objects

<img src="slides/lecture1/images/InstanceCube.png" width="40%">

- the following example shows the use of Patches and Object instancing in RIB

+++?code=Lecture1Intro/InstanceCube.rib&lang=python&title=[InstanceCube.rib](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/InstanceCube.rib)
@[7](Declare and identifier for our object)
@[8-15](The following elements will form our instance)
@[24,29,35](Instance the Cube Objects)

+++

## Python Cube Function
<img src="slides/lecture1/images/Cube2.png" width="30%">
- The previous example used the Object instance rib command
- This allowed us to repeat a series of rib commands.
- with python this can be replaced with a python function instead

+++?code=Lecture1Intro/Cube.py&lang=python&title=[Cube.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/Cube.py)
@[6-17](Define the cube function with default unit size arguments)
@[58-63](Call the cube function notice the use of Skew here)

---

## Adding Colour
- Before the introduction of RIS colour changes were controlled by the RiColor command
- For example to create a red object we use ```Color 1 0 0```
- Colour is an attribute and as such will remain the currently active colour until changed.
- To group colours (or any other attributes) we use the AttributeBegin and AttributeEnd block

+++

## RIS
- Since the introduction of RIS the Color command no longer works
- As of Renderman 21 

> The default hider is "raytrace", default bxdf is [PxrDiffuse](https://renderman.pixar.com/resources/RenderMan_20/devExamples.html#pxrdiffuse), and the default integrator is [PxrDefault](https://renderman.pixar.com/resources/RenderMan_20/PxrDefault.html).

+++

## PxrDefault

- The default integrator places a virtual light at the camera (the "headlamp integrator"). 
- No shadows or indirect lighting are evaluated. 
  - A good option when all is black - this integrator can help narrow down where a problem is occurring 
- Like PxrDirectLighting, it is not designed to produce "final-quality" images.

+++

## ri.BxDF 

- To specify a surface material we use the BxDF rib statement

```
Bxdf "Material Name" "label" "parameters"

```

- in python we use 

```python
ri.Bxdf( 'PxrDiffuse','diffuse', 
{
'color diffuseColor' : [ 1.0, 0.0, 1.0]
})
```
@[3] Notice the python dictionary for paramaters


