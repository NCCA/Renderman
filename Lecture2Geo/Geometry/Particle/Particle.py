import sys
import math
import getpass
import time
import prman


class Particle :
	Colour=[]
	Position=[]
	Direction=[]
	Life=0
	EndLife=0
	Width=0.02
	# ctor to assign values
	def __init__(self, Pos,Colour,Direction,EndLife,Width):
		self.Position=Pos
		self.Colour=Colour
		self.Direction=Direction
		self.EndLife=EndLife
		self.Width=Width
		
	def Update(self) :
		self.Position[0]+=self.Direction[0]
		self.Position[1]+=self.Direction[1]
		self.Position[2]+=self.Direction[2]
		self.Life+=1
		if self.Life > self.EndLife :
			self.Life=0
			self.Position=[0,0,0]
			
