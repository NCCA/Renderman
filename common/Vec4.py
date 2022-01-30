import math

################################################################################
# Simple Vector class
# x,y,z,w attributes for vector data
################################################################################


class Vec4:
    # ctor to assign values
    def __init__(self, x, y, z, w=1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    # debug print function to print vector values
    def __str__(self):
        return "[", self.x, ",", self.y, ",", self.z, ",", self.w, "]"

    # overloaded sub operator subtract (self - rhs) returns another vector
    def __sub__(self, rhs):
        return Vec4(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z, self.w)

    # overloaded sub operator subtract (self - rhs) returns another vector
    def __add__(self, rhs):
        return Vec4(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z, self.w)

    # Cross product of self with rhs returns another Vector
    def cross(self, rhs):
        return Vec4(
            self.y * rhs.z - self.z * rhs.y, self.z * rhs.x - self.x * rhs.z, self.x * rhs.y - self.y * rhs.x, 0.0
        )

    # Normalize vector to unit length (acts on itself)
    def normalize(self):
        len = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if len != 0:
            self.x /= len
            self.y /= len
            self.z /= len

    # simple dot product of self and rhs value n
    def dot(self, n):
        return (self.x * n.x) + (self.y * n.y) + (self.z * n.z)
