import math

class Mat4 :
  def __init__(self):
    self.m=[1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0]

  def __str__(self) :
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

