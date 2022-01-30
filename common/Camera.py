# import the python renderman library
import prman
from Vec4 import Vec4
import math


class Camera:
    def __init__(self, eye, look, up):
        # now construct the cameras viewing vectors N is eye-look
        self.U = Vec4(1, 0, 0, 1)
        self.V = Vec4(0, 1, 0, 1)
        self.N = Vec4(0, 0, 1, 1)
        self.eye = Vec4(0, 0, 0, 1)
        self.eye = eye
        self.buildUVN(eye, look, up)

    def buildUVN(self, eye, look, up):
        self.N = eye - look
        # now construct another orthogonal to the N
        self.U = up.cross(self.N)
        # and finally the  new up vector
        self.V = self.N.cross(self.U)
        # normalize the vectors to unit length
        self.N.normalize()
        self.U.normalize()
        self.V.normalize()

    def place(self, ri):
        U = self.U
        V = self.V
        N = self.N
        eye = self.eye
        ri.Identity()
        ri.Scale(1, 1, -1)
        tx = [U.x, V.x, N.x, 0.0, U.y, V.y, N.y, 0.0, U.z, V.z, N.z, 0.0, -eye.dot(U), -eye.dot(V), -eye.dot(N), 1.0]
        ri.ConcatTransform(tx)

    def slide(self, du, dv, dn):
        self.eye.x += du * self.U.x + dv * self.V.x + dn * self.N.x
        self.eye.y += du * self.U.y + dv * self.V.y + dn * self.N.y
        self.eye.z += du * self.U.z + dv * self.V.z + dn * self.N.z
