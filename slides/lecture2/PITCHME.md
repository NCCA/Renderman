## Geometry in Renderman

#### using the python api

---

## The Obj File format

- @size[smaller](Alias Wavefront obj files define the geometry and other properties for objects which can be easily used within animation packages. )
- @size[smaller](Object files can be in ASCII format .obj or binary format .mod.) 
- @size[smaller](For simplicity the ASCII format will be discussed here as it is easier to parse the data and is a good exercise for file and string handling. )
- @size[smaller](In its current release, the .obj file format supports both polygonal objects and free-form objects such as curves, nurbs etc.) 

+++

## File Format

- The following types of data may be included in an .obj file. In this list, the keyword (in parentheses) follows the data type.

  - geometric vertices (v)
  - texture vertices (vt)
  - vertex normals (vn)
  - face (f)

+++

## File Format
- group name (g)
- smoothing group (s)
- material name (usemtl)
- material library (mtllib)
- all values are stored on a single line terminated with a \n (new line character)

+++

## Face Format

- A valid vertex index matches the corresponding vertex elements of a previously defined vertex list.

```
f v1 v2 v3 ....
f v1/vt1 v2/vt2 v3/vt3 ...
f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3 ...
f v1//vn1 v2//vn2 v3//vn3 ...
```
- It is also possible to reference points using negative indices, where the indices are specified relative to the current maximum vertex position (-1 references the last vertex defined). 

+++

## Face Format

- This makes it easy to describe the points in a face, then the face, without the need to store a large list of points and their indexes. In this way, "v" commands and "f" commands can be interspersed.

```
v -0.500000 0.000000 0.400000
v -0.500000 0.000000 -0.800000
v -0.500000 1.000000 -0.800000
v -0.500000 1.000000 0.400000
f -4 -3 -2 -1

```

---

## Python Obj Loader

<img src="slides/lecture2/images/Obj.png" width="30%">

- The python obj class is passed a file name and loads the obj file data into a number of lists
- These are then made available to a number of methods which produced renderman output for rendering


+++?code=common/Obj.py&lang=python&title=Obj.py

+++?code=Lecture2Geo/Obj2Rib/ObjTest.py&lang=python&title=ObjTest.py

---

## Polygons
- The RenderMan Interface supports two basic types of polygons: 
  - a convex polygon and a general concave polygon with holes. 
- In both cases the polygon must be planar. 
- Collections of polygons can be passed by giving a list of points and an array that indexes these points. 
- The geometric normal of the polygon is computed by computing the normal of the plane containing the polygon (unless it is explicitly specified). 

+++

## Normals

- If the current orientation is left-handed, then a polygon whose vertices were specified in clockwise order (from the point of view of the camera) will be a front-facing polygon (that is, will have a normal vector which points toward the camera). 
- If the current orientation is right-handed, then polygons whose vertices were specified in counter clockwise order will be front-facing. - The shading normal is set to the geometric normal unless it is explicitly specified at the vertices.

+++

## ri.Polygon

- Polygons are specified with the riPolygon function. 
- The parameter list must include at least position ("P") information. 

```
points=[-1,-1,0,0,1,0,1,-1,0]
normals=[0,0,-1,0,0,-1,0,0,-1]
tx=[0,1,0.5,0,1,1]
ri.Polygon({ri.P:points,ri.N:normals,ri.ST:tx})

Polygon "varying float[2] st" [0 1 0.5 0 1 1] "vertex point P" [-1 -1 -2 0 1 1 1 -1 0] "varying normal N" [0 0 -1 0 0 -1 0 0 -1]
```

+++

## ri.GeneralPolygon
<img src="slides/lecture2/images/General.png" width="30%">

- Define a general planar concave polygon with holes. This polygon is specified by giving nloops lists of vertices. 
- The first loop is the outer boundary of the polygon; all additional loops are holes.

+++

## ri.PointsPolygon

- @size[smaller](Define npolys planar convex polygons that share vertices. )
- @size[smaller](The array nvertices contains the number of vertices in each polygon and has length npolys.) 
- @size[smaller](The array vertices contains, for each polygon vertex, an index into the varying primitive variable arrays.) 
- @size[smaller](The varying arrays are 0-based. vertices has length equal to the sum of all of the values in the nvertices array.) 
- @size[smaller](Individual vertices in the parameterlist are thus accessed indirectly through the indices in the array vertices. )

+++

## ri.PointsPolygon

```
points=[-0.5,-0.5,-0.5,
     0.5,-0.5,-0.5,
    -0.5, 0.5,-0.5,
     0.5, 0.5,-0.5,
    -0.5,-0.5, 0.5,
     0.5,-0.5, 0.5,
    -0.5, 0.5, 0.5,
     0.5, 0.5, 0.5]
npolys=[4,4,4,4,4,4]
nvertices=[0,2,3,1,0,1,5,4,0,4,6,2,1,3,7,5,2,6,7,3,4,5,7,6]
ri.PointsPolygons(npolys,nvertices,{ri.P:points})

```

+++

## ri.PointsGeneralPolygons

- Define npolys general planar concave polygons, with holes, that share vertices. 
- The array nloops indicates the number of loops comprising each polygon and has a length npolys. 
- The array nvertices contains the number of vertices in each loop and has a length equal to the sum of all the values in the array nloops. 
- The array vertices contains, for each loop vertex, an index into the varying primitive variable arrays.

---

## ri.Points & ri.Curves

- The RenderMan Interface includes lightweight primitives for specifying point clouds, lines, curves, or ribbons. 
- These primitives are especially useful for representing many particles, hairs, etc.

+++

## ri.Points

- Draws npoints number of point-like particles. 
- parameterlist is a list of token-array pairs where each token is one of the standard geometric primitive variables, a variable that has been defined with RiDeclare, or is given as an inline declaration. 
- The parameter list must include at least position ("P") information, one value for each particle. 

+++

## ri.Points

<img src="slides/lecture2/images/points.png" width="30%">


- If a primitive variable is of class varying or vertex, the array contains npoints data values of the appropriate type, i.e., one per particle. 
- If the variable is uniform or constant, the array contains a single element. 

+++

## ri.Curves
- Draws ncurves number of lines, curves, or ribbon-like particles of specified width through a set of control vertices. 
- Multiple disconnected individual curves may be specified using one call to RiCurves. 
- The parameter ncurves is the number of individual curves specified by this command
- nvertices is an array of length ncurves integers specifying the number of vertices in each of the respective curves.


+++

## ri.Curves

- The interpolation method given by type can be either "linear" or "cubic". 
- Cubic curves interpolate using the v basis matrix and step size set by RiBasis. 
- The u parameter changes across the width of the curve, whereas the v parameter changes across the length of the curve (i.e., the direction specified by the control vertices). 
- Curves may wrap around in the v direction, depending on whether wrap is "periodic" or "nonperiodic". 
- Curves that wrap close upon themselves at the ends and the first control points will be automatically repeated. As many as three control points may be repeated, depending on the basis matrix of the curve. 


---

## Procedural Primitives

- Procedural primitives allow use to call a helper program which generates geometry on-the-fly in response to procedural primitive requests in the RIB stream. 
- Each generated procedural primitive is described by a request to the helper program, in the form of an ASCII datablock which describes the primitive to be generated. 

+++

## Procedural Primitives

- This datablock can be anything which is meaningful and adequate to the helper program, such as a sequence of a few floating point numbers, a filename, or a snippet of code in a interpreted modeling language. 
- In addition the renderer supplies the detail of the primitive's bounding box, so that the generating program can make decisions on what to generate based on how large the object will appear on-screen.

+++

## Procedural Primitives

- The generation program reads requests on its standard input stream, and emits RIB streams on its standard output stream. 
- These RIB streams are read into the renderer as though they were read from a file (as with ReadArchive ), and may include any standard RenderMan attributes and primitives (including procedural primitive calls to itself or other helper programs). 

+++

## Procedural Primitives

- As long as any procedural primitives exist in the rendering database which require the identical helper program for processing, the socket connection to the program will remain open. 
- This means that the program should be written with a loop which accepts any number of requests and generates a RIB "snippet" for each one.

+++

## Procedural Primitives

- The specific syntax of the request from the renderer to the helper program is extremely simple, as follows:

```
fprintf(socket, "%g %s\n", detail, datablock);
```
- The detail is provided first, as a single floating-point number, followed by a space, followed by the datablock and finally a newline. 

- The datablock is completely uninterpreted by the renderer or by the socket write, so any newlines or special characters should be preserved 

+++

## Procedural Primitives
- The helper program's response should be to create a RIB file on stdout, 
```
RiBegin(RI_NULL);
   RiAttributeBegin();
     // various attributes
     // various primitives
   RiAttributeEnd();
 RiArchiveRecord(RI_COMMENT,"\377");
RiEnd();
```

+++

## Procedural Primitives
- Notice, in particular, the special trick which the helper program must use to stay in synchronized communication with the renderer.
- stdout should not be closed when the RIB snippet is complete, but rather a single '\377' character should be emitted and the stdout stream flushed. 
- This will signal the renderer that this particular snippet is complete, yet leave the stream open in order to write the next snippet. 

+++

## Procedural Primitives

- The use of RiArchiveRecord and RiEnd as above will accomplish this when the RIB client library is used.
- Warning: if the '\377' character is not emitted, nor is accidentally not flushed through the stdout pipe to the renderer, the render will hang.
- When the renderer is done with the helper program, it will close its end of the IPC socket, so reading an EOF on stdin is the signal for the helper program to exit.

+++

## Procedural Primitives

- In RIB, the syntax for specifying a RIB-generating program procedural primitive is:

```
Procedural "RunProgram" [ "program" "datablock" ] [ bound ]
```
- program is the name of the helper program to execute, and may include command line options. 
- datablock is the generation request data block. It is an ASCII string which is meaningful to program, and adequately describes the children which are to be generated. 
- The bound is an array of six floating point numbers which is xmin, xmax, ymin, ymax, zmin, zmax in the current object space.


---

## references
- Renderman documentation
- Using Procedural Primitives in PhotoRealistic RenderMan
- PRMan for Python — A Bridge from PRMan to Python (and Back)
- http://www.fileformat.info/format/wavefrontobj/
- App not #19 Using the RiCurves Primitive
- http://docs.python.org/
- Appendix D - RenderMan Interface Bytestream Conventions
- Application Note #3 How To Render Quickly Using PhotoRealistic RenderMan