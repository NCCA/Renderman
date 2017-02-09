import math

class Mat4 :
  def __init__(self):
    self.m=[1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0]

  def __str__(self) :
    return "[%f %f %f %f]\n[%f %f %f %f]\n[%f %f %f %f]\n[%f %f %f %f]\n" %(self.m[0],self.m[1],self.m[2],self.m[3],
    self.m[4],self.m[5],self.m[6],self.m[7],self.m[8],
    self.m[9],self.m[10],self.m[11],self.m[12],self.m[13],self.m[14],self.m[15])
    return str(self.m)

  def identity(self) :
    self.m=[1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0]   

  def rotateX(self,deg) :
    beta=math.radians(deg)
    sr = math.sin( beta );
    cr = math.cos( beta );
    self.m[5] =  cr;
    self.m[9] = -sr;
    self.m[6] =  sr;
    self.m[10] =  cr;

  def rotateY(self,deg) :
    beta=math.radians(deg)
    sr = math.sin( beta );
    cr = math.cos( beta );
    self.m[0] =  cr;
    self.m[8] =  sr;
    self.m[2] = -sr;
    self.m[10] =  cr;

  def rotateZ(self,deg) :
    beta=math.radians(deg)
    sr = math.sin( beta );
    cr = math.cos( beta );
    self.m[0] =  cr;
    self.m[4] =  -sr;
    self.m[1] = sr;
    self.m[5] =  cr;


  def translate(self,x,y,z) :
    self.m[12]=x
    self.m[13]=y
    self.m[14]=z

  def scale(self,x,y,z) :
    self.m[0]=x
    self.m[5]=y
    self.m[10]=z

  def transpose(self ) :
    tmp=Mat4()
    tmp.m=[ 
       self.m[0],self.m[4],self.m[8 ],self.m[12],
       self.m[1],self.m[5],self.m[9 ],self.m[13],
       self.m[2],self.m[6],self.m[10],self.m[14],
       self.m[3],self.m[7],self.m[11],self.m[15] ]
    self.m=tmp.m
    return tmp