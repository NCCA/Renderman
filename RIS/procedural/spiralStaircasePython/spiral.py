#!/usr/bin/python

######################################################################
# spiral.py Renderman Procedural Usage
# Procedural 'RunProgram' ['spiral.py' 'w h d H A'] [Bounding Box]
# Parameters Width Height Depth of Stair block
# Height of stairs
# Angle of stair Rotation
#
######################################################################


import sys

# grab the function ptr to write should speed things up.
Write = sys.stdout.write

######################################################################
# Function to draw a block made from Patches
# The center of the block if w/2 d/2 h/2
######################################################################


def Block(width, hight, depth):
    Write("TransformBegin\n")
    w = width / 2.0
    h = hight / 2.0
    d = depth / 2.0
    # rear face
    Write("Translate %f %f 0" % (w, h))
    Write("	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (-w, -h, d, -w, h, d, w, -h, d, w, h, d))
    # front face
    Write(
        "	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (-w, -h, -d, -w, h, -d, w, -h, -d, w, h, -d)
    )

    # left face
    Write(
        "	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (-w, -h, -d, -w, h, -d, -w, -h, d, -w, h, d)
    )
    # right face
    Write("	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (w, -h, -d, w, h, -d, w, -h, d, w, h, d))
    # bottom face
    Write(
        "	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (w, -h, d, w, -h, -d, -w, -h, d, -w, -h, -d)
    )

    # top face
    Write("	Patch 'bilinear' 'P' [%f %f %f %f %f %f %f %f %f %f %f %f   ]" % (w, h, d, w, h, -d, -w, h, d, -w, h, -d))
    Write("TransformEnd\n")


###############################################
# Signal to prman that we have finished (\377) and
# print out error message on stderr
################################################
def NiceExit(message):
    sys.stderr.write(message)
    # flush stream so prman knows we are done
    Write("\377")
    sys.stdout.flush()


###############################################################################################
# prman RunPrograms must read in a the data from stdin in the format
# The detail is provided first, as a single floating-point number, followed by a space,
# followed by the datablock and finally a newline.
# The datablock is completely uninterpreted by the renderer or by the socket write,
# so any newlines or special characters should be preserved
# (but the quotation marks that make it a string in the RIB file will, of course, be missing).
###############################################################################################

if __name__ == "__main__":
    # get the datablock from prman
    args = sys.stdin.readline()
    # now loop round as we may get more data
    while args:
        # split the  data into blocks
        words = args.split()
        # the first is the detail (a float)
        detail = float(words[0])
        # now check  to see if we have enough arguments
        if len(words) < 6:
            NiceExit("Error in ribfile not enough arguments\n Args were %s" % args)
            break
        # so we have enough arguments so extract the detail we need
        else:
            # first get the datablock from prman
            datablock = words[1:]
            # and extract the data we need
            width = float(datablock[0])
            height = float(datablock[1])
            depth = float(datablock[2])
            StairHeight = float(datablock[3])
            RotationAngle = float(datablock[4])
            # do an explicit TransformBegin
            Write("TransformBegin\n")
            # now the center cylinder
            Write("Translate 0 -1 0\n")
            Write("Rotate -90 1 0 0\n")
            size = StairHeight + (3 * height)
            Write("Cylinder 0.2  %f 1 360\n" % (size))
            sys.stderr.write("%f \n" % (size))
            Write("TransformEnd\n")

            # now we do some calculations and make our spiral
            i = 0.0
            Write("TransformBegin\n")
            # loop and build the blocks
            while i <= StairHeight:
                Block(width, height, depth)
                Write("Translate 0 %f 0\n" % height)
                Write("Rotate %f 0 1 0\n" % RotationAngle)
                i += height
            Write("TransformEnd\n")

            # we now close the rib stream and get the  next datablock  if there  is  one

            Write("\377")
            sys.stdout.flush()
        # read the next line
        args = sys.stdin.readline()
