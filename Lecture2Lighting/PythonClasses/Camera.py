# import the python renderman library
import prman
from vector import *
import math

class Camera :
	U=Vector(1,0,0,1)
	V=Vector(0,1,0,1)
	N=Vector(0,0,1,1)
	eye=Vector(0,0,0,1)
	fov=50
	Width=720
	Height=576
	PixelAspect=1.0
	fstop=16
	focallength=8
	focaldistance=10
	shutter =[0,1]
	def __init__(self, eye,look,up):
		# now construct the cameras viewing vectors N is eye-look
		self.eye=eye
		self.BuildUVN(eye,look,up)


	def BuildUVN(self,eye,look,up) :
		self.N=eye-look
		# now construct another orthogonal to the N
		self.U=up.Cross(self.N)
		# and finally the  new up vector
		self.V=self.N.Cross(self.U)
		# normalize the vectors to unit length
		self.N.normalize()
		self.U.normalize()
		self.V.normalize()


	def Place(self,ri):
		U=self.U
		V=self.V
		N=self.N
		eye=self.eye
		ri.Identity();
		ri.Scale(1,1,-1)
		tx=[U.x,V.x,N.x,0.0,U.y,V.y,N.y,0.0,U.z,V.z,N.z,0.0,-eye.dot(U),-eye.dot(V),-eye.dot(N),1.0]	
		ri.ConcatTransform(tx)

	def Format(self,ri) :
		ri.Format(self.Width,self.Height,self.PixelAspect)
		# now set the projection to perspective
		ri.Projection(ri.PERSPECTIVE,{ri.FOV: self.fov}) 
		
	def Slide(self,du,dv,dn) :
		self.eye.x += du * self.U.x + dv * self.V.x + dn * self.N.x;
		self.eye.y += du * self.U.y + dv * self.V.y + dn * self.N.y;
		self.eye.z += du * self.U.z + dv * self.V.z + dn * self.N.z;
		
	def dof(self,ri) :
		ri.DepthOfField(self.fstop,self.focallength,self.focaldistance)
		
	def Shutter(self,ri,min,max) :
		self.shutter=[min,max]
		ri.Shutter(min,max)


