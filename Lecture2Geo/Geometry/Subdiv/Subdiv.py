#!/usr/bin/env rmanpy
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "PointPolygon.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Subdiv.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 4)
ri.Rotate(-15, 1, 0, 0)
ri.TransformBegin()

# create a simple checker pattern
expr = """
$colour = c1;
$c = floor( 10 * $u ) +floor( 10 * $v );
if( fmod( $c, 2.0 ) < 1.0 )
{
	$colour=c2;
}
$colour
"""


# all the indices are the same ammount
npolys = [4] * 6
points = [
    -0.5,
    -0.5,
    -0.5,  # 0
    0.5,
    -0.5,
    -0.5,  # 1
    -0.5,
    0.5,
    -0.5,  # 2
    0.5,
    0.5,
    -0.5,  # 3
    -0.5,
    -0.5,
    0.5,  # 4
    0.5,
    -0.5,
    0.5,  # 5
    -0.5,
    0.5,
    0.5,  # 6
    0.5,
    0.5,
    0.5,
]  # 7
indices = [0, 1, 3, 2, 0, 4, 5, 1, 0, 2, 6, 4, 1, 5, 7, 3, 2, 3, 7, 6, 4, 6, 7, 5]  # 0  # 1  # 2  # 3  # 4  # 5

# use the pattern
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [1, 0, 0], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)

ri.TransformBegin()
ri.Translate(-1.5, 0, 0)
ri.Rotate(45, 0, 1, 0)
ri.SubdivisionMesh(
    "catmull-clark",
    npolys,
    indices,
    [ri.CREASE, ri.CREASE, ri.CREASE, ri.CREASE],
    [5, 1, 5, 1, 5, 1, 5, 1],
    [4, 5, 7, 6, 4, 0, 1, 3, 2, 0, 0, 4, 6, 2, 0, 1, 5, 7, 3, 1],
    [3, 3, 3, 3],
    {ri.P: points},
)

ri.TransformEnd()


# use the pattern
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 0], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)
ri.TransformBegin()
ri.Translate(0, 0, 0)
ri.Rotate(45, 0, 1, 0)
ri.SubdivisionMesh(
    "catmull-clark",
    npolys,
    indices,
    [ri.CREASE, ri.CREASE, ri.CREASE, ri.CREASE],
    [5, 1, 5, 1, 5, 1, 5, 1],
    [4, 5, 7, 6, 4, 0, 1, 3, 2, 0, 0, 4, 6, 2, 0, 1, 5, 7, 3, 1],
    [1, 1, 1, 1],
    {ri.P: points},
)

ri.TransformEnd()


# use the pattern
ri.Pattern("PxrSeExpr", "seTexture", {"color c1": [1, 1, 1], "color c2": [0, 0, 1], "string expression": [expr]})
ri.Bxdf(
    "PxrDiffuse",
    "diffuse",
    {
        #  'color diffuseColor'  : [1,0,0]
        "reference color diffuseColor": ["seTexture:resultRGB"]
    },
)
ri.TransformBegin()
ri.Translate(1.5, 0, 0)
ri.Rotate(45, 0, 1, 0)
ri.SubdivisionMesh(
    "catmull-clark",
    npolys,
    indices,
    [ri.CREASE, ri.CREASE, ri.CREASE, ri.CREASE],
    [5, 1, 5, 1, 5, 1, 5, 1],
    [4, 5, 7, 6, 4, 0, 1, 3, 2, 0, 0, 4, 6, 2, 0, 1, 5, 7, 3, 1],
    [10, 10, 10, 10],
    {ri.P: points},
)

ri.TransformEnd()

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
