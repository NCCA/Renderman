## Geometry in Renderman

#### using the python api

---

## The Obj File format

- Alias Wavefront obj files define the geometry and other properties for objects which can be easily used within animation packages. 
- Object files can be in ASCII format (.obj) or binary format (.mod). 
- For simplicity the ASCII format will be discussed here as it is easier to parse the data and is a good exercise for file and string handling. 
- In its current release, the .obj file format supports both polygonal objects and free-form objects such as curves, nurbs etc. 

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


+++?code=PythonClasses/Obj.py&lang=python&title=Obj.py

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

- Define npolys planar convex polygons that share vertices. 
- The array nvertices contains the number of vertices in each polygon and has length npolys. 
- The array vertices contains, for each polygon vertex, an index into the varying primitive variable arrays. 
- The varying arrays are 0-based. vertices has length equal to the sum of all of the values in the nvertices array. 
- Individual vertices in the parameterlist are thus accessed indirectly through the indices in the array vertices. 

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