#!/usr/bin/python

from Mat4 import *

a = Mat4()
print(a)
a.rotateX(45)
print(a)
a.identity()
a.rotateY(45)
print(a)
a.identity()
a.rotateZ(45)
print(a)
a.identity()
a.scale(2, 2, 2)
a.translate(3, 4, 5)
print(a)
a.transpose()
print(a)
print(a.getTranspose())
print(a * a.getTranspose())
