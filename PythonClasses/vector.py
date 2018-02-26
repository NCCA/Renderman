import sys
import math
import getpass
import time

################################################################################
# Simple Vector class
# x,y,z,w attributes for vector data
################################################################################

class Vector:
	# ctor to assign values
	def __init__(self, x, y, z,w):
		self.x=float(x)
		self.y=float(y)
		self.z=float(z)
		self.w=float(1.0)
	# debug print function to print vector values
	def Print(self):
		print "[",self.x,",",self.y,",",self.z,",",self.w,"]"
	# overloaded sub operator subtract (self - rhs) returns another vector
	def __sub__(self, rhs):
		return Vector(self.x - rhs.x,self.y - rhs.y,self.z - rhs.z,self.w)
	# Cross product of self with rhs returns another Vector
	def Cross(self,rhs):
		return Vector(self.y*rhs.z - self.z*rhs.y, self.z*rhs.x - self.x*rhs.z, self.x*rhs.y - self.y*rhs.x,0.0)
	# Normalize vector to unit length (acts on itself)
	def normalize(self):
			len=math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
			#print "Len = ",len
			#print "vect orig %f %f %f" %(self.x,self.y,self.z)

			if(len !=0) :
				self.x/=len 
				self.y/=len 
				self.z/=len
			#print "vect %f %f %f" %(self.x,self.y,self.z)
	# simple dot product of self and rhs value n
	def dot(self,n) :
		return ((self.x * n.x) + (self.y * n.y) + (self.z * n.z))

