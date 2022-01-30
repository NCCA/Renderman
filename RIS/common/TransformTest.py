#!/usr/bin/python
from Transformation import *

tx = Transformation()
tx.setPosition(1, 2, 3)
tx.setRotation(45, 12, 22)
tx.setScale(1.0, 0.2, 1.0)
print(tx.getMatrix())
