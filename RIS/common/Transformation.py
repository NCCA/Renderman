from Mat4 import *
from Vec4 import *


class Transformation:
    def __init__(self):
        self.matrix = Mat4()
        self.position = Vec4(0.0, 0.0, 0.0)
        self.scale = Vec4(1.0, 1.0, 1.0)
        self.rotation = Vec4(0.0, 0.0, 0.0)
        self.isComputed = False

    def getMatrix(self):
        if self.isComputed == False:
            self.computeMatrix()
        return [item for sublist in self.matrix.m for item in sublist]
        # return self.matrix

    def setPosition(self, x, y, z):
        self.isComputed = False
        self.position.x = x
        self.position.y = y
        self.position.z = z

    def setScale(self, x, y, z):
        self.isComputed = False
        self.scale.x = x
        self.scale.y = y
        self.scale.z = z

    def setRotation(self, x, y, z):
        self.isComputed = False
        self.rotation.x = x
        self.rotation.y = y
        self.rotation.z = z

    def computeMatrix(self):
        scale = Mat4()
        rX = Mat4()
        rY = Mat4()
        rZ = Mat4()
        scale.scale(self.scale.x, self.scale.y, self.scale.z)
        rX.rotateX(self.rotation.x)
        rY.rotateY(self.rotation.y)
        rZ.rotateZ(self.rotation.z)
        self.matrix = scale * rX * rY * rZ
        self.matrix.m[3][0] = self.position.x
        self.matrix.m[3][1] = self.position.y
        self.matrix.m[3][2] = self.position.z
        self.matrix.m[3][3] = 1.0

        self.isComputed = True
