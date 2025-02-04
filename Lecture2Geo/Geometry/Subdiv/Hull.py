#!/usr/bin/env rmanpy
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Hull.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Hull.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 150)
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


points = [
    -60,
    60,
    0,
    -60,
    20,
    0,
    -60,
    -20,
    0,
    -60,
    -60,
    0,
    -20,
    60,
    0,
    -20,
    20,
    45,
    -20,
    -20,
    45,
    -20,
    -60,
    0,
    20,
    60,
    0,
    20,
    20,
    45,
    20,
    -20,
    45,
    20,
    -60,
    0,
    60,
    60,
    0,
    60,
    20,
    0,
    60,
    -20,
    0,
    60,
    -60,
    0,
]

ri.Rotate(45, 1, 0, 0)
ri.Rotate(180, 0, 1, 0)
ri.SubdivisionMesh(
    "catmull-clark",
    [4, 4, 4, 4, 4, 4, 4, 4, 4],
    [
        0,
        4,
        5,
        1,
        1,
        5,
        6,
        2,
        2,
        6,
        7,
        3,
        4,
        8,
        9,
        5,
        5,
        9,
        10,
        6,
        6,
        10,
        11,
        7,
        8,
        12,
        13,
        9,
        9,
        13,
        14,
        10,
        10,
        14,
        15,
        11,
    ],
    [ri.INTERPBOUNDARY],
    [0, 0],
    [],
    [],
    {ri.P: points},
)

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
