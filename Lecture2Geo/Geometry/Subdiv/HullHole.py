#!/usr/bin/env rmanpy
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "HullHole.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")  # filename)
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("HullHole.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 5)
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

"""
points=[-2,-2,0,
				-2, 2,0,
				 2, 2,0,
				 2,-2,0,
				-1,-1,0,
				 0,1,0,
				 1,-1,0]

ri.Rotate(45,1,0,0)
ri.Rotate(180,0,1,0)
ri.SubdivisionMesh("catmull-clark", 
										[4,3], 
										 [0,1,2,3,4,5,6], [ri.HOLE],[0,0],[],[],
									   {ri.P: points})
"""
# ri.Rotate(25,1,0,0)
# ri.Rotate(180,0,1,0)

ri.HierarchicalSubdivisionMesh(
    "catmull-clark",
    [4, 4, 4, 4, 4, 4, 4, 4, 4],
    [
        4,
        5,
        1,
        0,
        5,
        6,
        2,
        1,
        6,
        7,
        3,
        2,
        8,
        9,
        5,
        4,
        9,
        10,
        6,
        5,
        10,
        11,
        7,
        6,
        12,
        13,
        9,
        8,
        13,
        14,
        10,
        9,
        14,
        15,
        11,
        10,
    ],
    ["interpolateboundary", "faceedit", "vertexedit"],
    [1, 0, 0, 4, 0, 1, 20, 12, 3],
    [2, 3, 4, 1, 1, 4, 4, 1, 1, 0, 4, 4, 1, 1, 1, 4, 4, 1, 1, 2, 4, 4, 1, 1, 3],
    [0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1],
    ["hole", "add", "P", "value"],
    {
        "P": [
            -1,
            -1,
            0,
            -0.333333,
            -1,
            0,
            0.333333,
            -1,
            0,
            1,
            -1,
            0,
            -1,
            -0.333333,
            0,
            -0.333333,
            -0.333333,
            0,
            0.333333,
            -0.333333,
            0,
            1,
            -0.333333,
            0,
            -1,
            0.333333,
            0,
            -0.333333,
            0.333333,
            0,
            0.333333,
            0.333333,
            0,
            1,
            0.333333,
            0,
            -1,
            1,
            0,
            -0.333333,
            1,
            0,
            0.333333,
            1,
            0,
            1,
            1,
            0,
        ]
    },
)


ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
