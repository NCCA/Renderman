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

- python version

```python
ri.Bxdf( 'PxrDiffuse','diffuse', 
{
'color diffuseColor' : [ 1.0, 0.0, 1.0]
})
```
@[3]( Notice the python dictionary for parameters)

+++?code=Lecture1Intro/Colour.py&lang=python&title=[Colour.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/Colour.py)
@[26-29](Here we use the simple PxrDiffuse surface model)

+++

## Using Patterns for Colour

- A call to ```PxrDiffuse``` can set the colour for the whole primitive
- If we wish to pass Colour as a parameter list we need some other way of reading the information
- We can do this using a combination of ```ri.Pattern``` and an OSL shader or a SeExpr expression.

+++?code=Lecture1Intro/Param.py&lang=python&title=[Param.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/Param.py)
@[23-27](Here we define the Pattern and the BxDF)
@[32](define a list of Colours (RGB Tuples))
@[33](Pass this to the Sphere command using the Variable Cs)

+++?code=Lecture1Intro/colour.osl&lang=python&title=[colour.osl](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/colour.osl)

+++

## [Using SeExpr](https://www.disneyanimation.com/technology/seexpr.html)

- SeExpr is a simple expression language which allows "Arithmetic expression of scalar/vector types"
- We can embed these within an ri.Pattern and read any of the built in parameter list variables such as ```Cs``` .

+++?code=Lecture1Intro/ParamSeExpr.py&lang=python&title=[ParamSeExpr.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/ParamSeExpr.py)
@[24-27](Define the expression in this case Cs is the output)
@[28-31](Use the output of the expression as the input to the diffuse resultRGB is the default)
@[36-37] (Pass Cs to the renderer)

---

### Rib file Structure Conventions

- Following is a structured list of components for a conforming RIB file that diagrams the "proper" use of RIB. 
- Some of the components are optional and will depend greatly on the resource requirements of a given scene. 
- Indentation indicates the scope of the following command.

+++

```
Preamble and global variable declarations (RIB requests:version,declare)
Static options and default attributes (image and display options,camera options) Static camera transformations (camera location and orientation)
Frame block (if more than one frame)
Frame-specific variable declarations Variable options and default attributes Variable camera transforms
World block
      (scene description)
      User Entity (enclosed within AttributeBegin/AttributeEnd)
      User Entity (enclosed within AttributeBegin/AttributeEnd)
      User Entity
more frame blocks
```

+++

## Rib file Structure

- This structure results from the vigorous application of the following Scoping Conventions:
- No attribute inheritance should be assumed unless implicit in the definition of the User Entity (i.e., within a hierarchy). 
- No attribute should be exported except to establish either global or local defaults. 

+++

## Rib file Structure

- The RenderMan Specification provides block structuring to organize the components of a RIB file. 
- Although the use of blocks is only required for frame and world constructs by the Specification, the liberal use of attribute and transform blocks is encouraged. 

+++

## Attributes

- Attributes are flags and values that are part of the graphics state, and are therefore associated with individual primitives. 
- The values of these attributes are pushed and popped with the graphics state.
- This is done with the ```AttributeBegin``` and ```AttributeEnd``` commands
- The attribute block is the fundamental block for encapsulating user entities. 

+++

## Attributes

- Within an attribute block, the structure is simple. All attribute settings should follow immediately after the AttributeBegin request.
- Geometric transformations are considered attributes in the RenderMan Interface and should also precede any geometry. 

+++

## Attributes

- Depending on the internal architecture of the modeling software, user entities may be described around a local origin. In this case, a modeling transformation commonly transforms the entity from object space to world space. 
- If this is not the case, the modeler will probably be working entirely in world space and no modeling transform will be present.
- After setting all of the attributes for the entity, the geometry should immediately follow

---

## Named Primitives

- It is occasionally useful to give names to individual primitives. For example, when a primitive won't split at the eye plane (see Section 4.8 prman docs) it can be desirable to know which primitive is causing the problem.This can be done using the attribute identifier with the parameter name, as in:

```
RtString name[1] = {"Gigi"};
RiAttribute("identifier","name",(RtPointer)name,RI_NULL);
or
Attribute "identifier" "name" ["Spheres3"]
```

+++

## Named Primitives

- All defined primitives will have this name until the graphics stack is popped (with RiAttributeEnd) or another such RiAttribute call is made. 
- The error message would then contain a reference to a specific primitive name instead of the mysterious <unnamed>.  

```python
ri.Attribute ("identifier",{"name": "Wave1"})
```

---

## Objects

- A single geometric primitive or a list of geometric primitives may be retained by enclosing them with ObjectBegin and ObjectEnd. 
- The RenderMan Interface allocates and returns an ObjectHandle for each retained object defined in this way. 
- This handle can subsequently be used to reference the object when creating instances with ObjectInstance. 

+++

## Objects 
- Objects are not rendered when they are defined within an ObjectBegin-ObjectEnd block; only an internal definition is created. 
- Transformations, and even Motion blocks, may be used inside an Object block, though they obviously imply a relative transformation to the coordinate system active when the Object is instanced. 

+++

## Objects 

- All of an object's attributes are inherited at the time it is instanced, not at the time at which it is created. 
- So, for example, shader assignments or other attributes are not allowed within an Object block. 

+++?code=Lecture1Intro/ObjBegin.py&lang=python&title=[ObjBegin.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/ObjBegin.py)
@[7-12](Simple Colour function)
@[41-49](Declare an Object and save the handle )
@[55-56] (Instance the Object)

---

## Options
- Options are parameters that affect the rendering of an entire image. 
- They must be set before calling WorldBegin, since at that point options for a specific frame are frozen.
- The PRMan Quick Reference includes a table that summarizes summarizes the options available in PhotoRealistic RenderMan. 
- Note that some of the defaults listed can be overridden by configuration files.

+++

## Frame Buffer Control
- There are several options which can be enabled through the parameter list of the RiDisplay call. 
- Output Compression
  - The TIFF driver also accepts an option to set the compression type, which may be "lzw", "packbits", "zip" (the default), "pixarlog", or "none":

```
Display "min.tiff" "TIFF" "rgba" "compression" "lzw"
```

+++

## OpenEXR Display Driver
-  This driver supports OpenEXR.
- When using this display driver for rgba or Z output, you should turn rgba and Z quantization off by using a floating point Quantize statement, ie:

```
Quantize "rgba" 0 0 0 0
Quantize "z"    0 0 0 0

ri.Quantize("rgba",0,0,0,0)
ri.Quantize("z",0,0,0,0)
```

+++

## OpenEXR Driver
-  This display driver also supports the output of image channels other than rgba using the Arbitrary Output Variable mechanisms.
- This driver maps Renderman's output variables to image channels as follows: 

+++

## OpenEXR Driver

|<small/>output variable name  |	<small/>image channel name | 	<small/>type|
|----------------------|---------------------|------|
|<small/>"r"	| <small/>"R"	| <small/>preferred type |
|<small/>"g"	| <small/>"G" | <small/>preferred type |
|<small/>"b"	| <small/>"B"	| <small/>preferred type |
|<small/>"a"	| <small/>"A"	| <small/>preferred type |
|<small/>"z"	| <small/>"Z"	| <small/>FLOAT |
| <small/>other	| <small/>same as output variable name	| <small/>preferred type |

+++

## Setting Display Parameters
- By default, the "preferred" channel type is the value  float (32-bit). 
- The preferred type can be changed by adding an ```"exrpixeltype"``` or ```"type"``` argument to the Display command in the RIB file.

``` python
# Store point positions in HALF format
Display "Points.exr" "openexr" "P" "string exrpixeltype" "half" 
ri.Display('Points.exr', 'openexr', 'P' ,{'string exrpixeltype' : 'half'})
```

+++

## Setting Display Parameters
 
- Compression defaults to "zip"
- You can select a different compression method by adding an "exrcompression" argument or simply the "compression" argument to the Display command. 

``` python
# Store RGBA using run-length encoding
Display "rle.rgba.exr" "openexr" "rgba" "string exrcompression" "rle" 
ri.Display('rle.rgba.exr', 'openexr', 'rgba' ,{'string exrcompression' :'rle'})
```

---

## Search Paths
- RenderMan searches specific paths for shader definitions, texture map files and other resources 
- The search path is a colon separated list of directories that are used in searching for files.

```
Option "searchpath" "string shader" ["/mapublic/shaders"]
ri.Option('searchpath', {'string shader':'/mapublic/shaders'})
```

+++

### Search Paths

- The valid search paths are:
  - shader :- Used by the renderer to find all shader files 
  - texture :- Used by the renderer to find all texture files 
  - archive :- Used by the renderer to find RIB archives 
  - procedural :- Used by the renderer to find procedural primitive DSO's 
  - display :- Used by the renderer to find display drivers

+++

### ReadArchive

- The ReadArchive command allows us to read another rib file into the current position of the RIB stream
- This can include zipped archives containing multiple archives

+++?code=Lecture1Intro/ReadArchive.py&lang=python&title=[ReadArchive.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/ReadArchive.py)
@[22](tell renderman where to search for the archive (relative path in this case))
@[51-52](Read the archive which will put the contents in the stream )


+++?code=Lecture1Intro/ReadZip.py&lang=python&title=[ReadZip.py](https://github.com/NCCA/Renderman/blob/master/Lecture1Intro/ReadZip.py)
@[22](tell renderman where to search for the archive we have created a zip file with the contents of this dir)
@[48-49](Read the archive using ! to specify the file within the zip )

---

## References
- [1] Ian Stephenson. Essential Renderman Fast. Springer-Verlag, 2003.
- [2] Larry Gritz Anthony A Apodaca. Advanced Renderman (Creating CGI for Motion Pictures). Morgan Kaufmann, 2000.
- Upstill S “The Renderman Companion” Addison Wesley 1992
- Renderman Documentation Appendix D - RenderMan Interface Bytestream Conventions
- Application Note #3 How To Render Quickly Using PhotoRealistic RenderMan
