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

### Lecture 1 [Intro to Renderman using the Python API](https://nccastaff.bournemouth.ac.uk/jmacey/Lectures/Renderman/Lecture1Introduction/#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture1Intro)


### Lecture 2 [Advanced Geometry :- Polygons, Subdivision surfaces, Points and Curves](https://nccastaff.bournemouth.ac.uk/jmacey/Lectures/Renderman/Lecture2Geometry/#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture2Geo)

### Lecture 3 [Lighting, Integrators and Materials in Renderman](https://nccastaff.bournemouth.ac.uk/jmacey/Lectures/Renderman/Lecture3Lighting/#/) [code](https://github.com/NCCA/Renderman/tree/master/Lecture3Lighting)


### AOV Examples [code](https://github.com/NCCA/Renderman/tree/master/AOV)


