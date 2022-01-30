import sys
import math
import getpass
import time
import prman
from Particle import *
import time, random


class Emitter:

    Position = []
    NumParticles = 0
    ParticleList = []
    # ctor to assign values
    def __init__(self, Pos, NumParticles):
        self.Position = Pos
        self.NumParticles = NumParticles
        # grab pointers to the random functions
        # this will speed up the loop as python will look it up each time
        ru = random.uniform
        ri = random.randint
        # same with the append
        ap = self.ParticleList.append
        for i in range(0, NumParticles):
            colour = [ru(0.1, 1.0), ru(0.1, 1.0), ru(0.1, 1.0)]
            Direction = [ru(-0.1, 0.1), ru(0.1, 0.2), ru(-0.1, 0.1)]
            EndLife = ri(8, 100)
            Width = ru(0.01, 0.2)
            ap(Particle(Pos, colour, Direction, EndLife, Width))

    def Update(self):
        # grab pointer to the particle list to speed lookups
        update = self.ParticleList
        for i in range(0, self.NumParticles):
            update[i].Update()

    def Draw(self, ri):
        points = []
        width = []
        colour = []
        # get pointers to the append functions to speed up loop
        pa = points.append
        wa = width.append
        ca = colour.append
        pl = self.ParticleList
        for i in range(0, self.NumParticles):
            pa(pl[i].Position[0])
            pa(pl[i].Position[1])
            pa(pl[i].Position[2])
            wa(pl[i].Width)
            ca(pl[i].Colour[0])
            ca(pl[i].Colour[1])
            ca(pl[i].Colour[2])

        ri.AttributeBegin()
        ri.Points({ri.P: points, "varying float width": width, "varying color Cs": colour})
        ri.AttributeEnd()
