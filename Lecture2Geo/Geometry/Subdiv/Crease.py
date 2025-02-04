#!/usr/bin/env rmanpy
# import the python renderman library
import prman


ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Crease.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Crease.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 576, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 4)
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

s = 1.0
points = [s, -s, -s, s, s, -s, s, -s, s, s, s, s, -s, s, s, -s, s, -s, -s, -s, s, -s, -s, -s]

ri.Rotate(45, 1, 1, 0)

ri.SubdivisionMesh(
    "catmull-clark",
    [4, 4, 4, 4, 4, 4],
    [0, 2, 3, 1, 4, 6, 7, 5, 5, 1, 3, 4, 2, 0, 7, 6, 6, 4, 3, 2, 1, 5, 7, 0],
    [ri.CREASE, ri.CREASE],
    [5, 1, 5, 1],
    [1, 5, 7, 0, 1, 3, 4, 6, 2, 3],
    [2, 2],
    {ri.P: points},
)

ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
