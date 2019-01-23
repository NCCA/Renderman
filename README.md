# RENDERMAN Lecture Code
The following lines need to be added to your .bashrc in the NCCA linux labs to get renderman to work

```
export RMANTREE=/opt/pixar/RenderManProServer-22.0/
export RMAN_SHADERPATH=$HOME/Shaders:$RMANTREE/lib/shaders
export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RMANTREE/lib:
export PATH=$PATH:$RMANTREE/bin
```


The following folders contain examples for my Renderman lectures. Note I'm in the process of updating these lectures to work with Renderman 22 and RIS so some of the content at present will not work.

### Lecture 1 [Intro to Renderman using the Python API](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/Lecture1Introduction/slides.html#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture1Intro)


### Lecture 2 [Advanced Geometry :- Polygons, Subdivision surfaces, Points and Curves](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/Lecture2Geometry/slides.html#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture2Geo)

### Lecture 3 [Lighting, Integrators and Materials in Renderman](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/Lecture3Lighting/slides.html#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture3Lighting)


### Old lectures PDF

### Lecture 2 [Using Lights and Cameras](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/LightingInRenderman.pdf) [code](https://github.com/NCCA/Renderman/tree/master/Lecture2Lighting)

### Lecture 3 [Advanced Geometry Polygons, Subdivision surfaces, Points and Curves, CSG , Animation](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/GeometryWithRenderman.pdf) [code](https://github.com/NCCA/Renderman/tree/master/Lecture3Geo)

### Lecture 4 [Basic Shaders](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/RendermanShaders1.pdf) [code](https://github.com/NCCA/Renderman/tree/master/Lecture4Shaders1)

### Lecture 5 [More Shaders](https://nccastaff.bournemouth.ac.uk/jmacey/Renderman/slides/RendermanShaders2.pdf) [code](https://github.com/NCCA/Renderman/tree/master/Lecture5Shaders2)

### AOV Examples [code](https://github.com/NCCA/Renderman/tree/master/AOV)


