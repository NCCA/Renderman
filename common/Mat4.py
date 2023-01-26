import math, operator,functools

""" simple 4x4 matrix class some code modified from here
http://code.activestate.com/recipes/578131-a-simple-matrix-class/
    
"""


class Mat4:
    def __init__(self):
        self.m = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        # self.rows = [[0]*4 for x in range(4)]

    def __str__(self):
        s = "\n".join([" ".join([str(item) for item in row]) for row in self.m])
        return s + "\n"

    def __getitem__(self, idx):
        return self.m[idx]

    def __setitem__(self, idx, item):
        self.m[idx] = item

    def identity(self):
        self.m = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

    def rotateX(self, deg):
        beta = math.radians(deg)
        sr = math.sin(beta)
        cr = math.cos(beta)
        self.m[1][1] = cr
        self.m[2][1] = -sr
        self.m[1][2] = sr
        self.m[2][2] = cr

    def rotateY(self, deg):
        beta = math.radians(deg)
        sr = math.sin(beta)
        cr = math.cos(beta)
        self.m[0][0] = cr
        self.m[2][0] = sr
        self.m[0][2] = -sr
        self.m[2][2] = cr

    def rotateZ(self, deg):
        beta = math.radians(deg)
        sr = math.sin(beta)
        cr = math.cos(beta)
        self.m[0][0] = cr
        self.m[1][0] = -sr
        self.m[0][1] = sr
        self.m[1][1] = cr

    def translate(self, x, y, z):
        self.m[3][0] = x
        self.m[3][1] = y
        self.m[3][2] = z

    def scale(self, x, y, z):
        self.m[0][0] = x
        self.m[1][1] = y
        self.m[2][2] = z

    def transpose(self):
        self.rows = [list(item) for item in zip(*self.m)]

    def getTranspose(self):
        mat = Mat4()
        mat.m = [list(item) for item in zip(*self.m)]

        return mat

    def getMatrix(self):
        return functools.reduce(operator.concat, self.m)

    def __mul__(self, rhs):
        mat_t = rhs.getTranspose()
        mulmat = Mat4()

        for x in range(4):
            for y in range(4):
                mulmat[x][y] = sum([item[0] * item[1] for item in zip(self.m[x], mat_t[y])])

        return mulmat

