#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random,math
# import the python renderman library
import prman



# Modified from Renderman Examples in The renderman Companion
# AimZ(): rotate the world so the direction vector points in
#	positive z by rotating about the y axis, then x. The cosine
#	of each rotation is given by components of the normalized
#	direction vector.  Before the y rotation the direction vector
#	might be in negative z, but not afterward.

def AimZ(ri,direction) :
	if (direction[0]==0 and direction[1]==0 and direction[2]==0) :
		return
	#
	# The initial rotation about the y axis is given by the projection of
	# the direction vector onto the x,z plane: the x and z components
	# of the direction.
	
	xzlen = math.sqrt(direction[0]*direction[0]+direction[2]*direction[2])
	if (xzlen == 0) :
		if(direction[1] <0) :
			yrot = 0
		else :
			yrot =180
	
	#		yrot = (direction[1] < 0) ? 180 : 0
	else :
		yrot = 180*math.acos(direction[2]/xzlen)/math.pi;
	
	
	 # The second rotation, about the x axis, is given by the projection on
	 # the y,z plane of the y-rotated direction vector: the original y
	 # component, and the rotated x,z vector from above.
	 
	yzlen = math.sqrt(direction[1]*direction[1]+xzlen*xzlen)
	xrot = 180*math.acos(xzlen/yzlen)/math.pi	 # yzlen should never be 0 
	
	if (direction[1] > 0) :
		ri.Rotate(xrot, 1.0, 0.0, 0.0)
	else :
		ri.Rotate(-xrot, 1.0, 0.0, 0.0)
	#The last rotation declared gets performed first 
	if (direction[0] > 0) :
		ri.Rotate(-yrot, 0.0, 1.0, 0.0)
	else :
		ri.Rotate(yrot, 0.0, 1.0, 0.0)
	


def ShadowPass(ri,Name,From,To,coneAngle,SceneFunc) :
	# 
	print "Rendering Shadow pass %s.z" %(Name)
	ri.Begin("__render")
	ri.Display(Name+".z", "zfile", "z")
	ri.Clipping(1,10)
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(512,512,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
	#now move to light position
	# create a vector for the Spotlight to and from values
	
	# to do this we subtract each of thelist elements using a lambda function
	# this is the same as doing the code below I will leave it to you as to which you
	# find more readable
	#direction =[To[0]-From[0],To[1]-From[1],To[2]-From[2]]
	
	direction = map(lambda x,y : x-y , To,From)
	AimZ(ri,direction)
	ri.Translate(-From[0],-From[1],-From[2])
	# now draw the Scene 
	ri.WorldBegin()
	SceneFunc(ri)
	ri.WorldEnd()
	ri.MakeShadow(Name+".z",Name+".shad",{ "minmax" :[1]})
	ri.End()
	print " Done MakeShadow %s.shad" %(Name)
	
	
def Scene(ri) :
	
	
	ri.Surface("plastic")
	ri.TransformBegin()
	ri.Translate( 0, -0.9, 0)
	ri.Scale( 1 ,0.4, 1)
	ri.Patch( "bilinear",{ "P" : [-0.5, -0.5, 0.5,-0.5, 0.5 ,0.5 ,0.5, -0.5, 0.5 ,0.5, 0.5, 0.5] })      
	ri.Patch( "bilinear",{ "P" :  [-0.5 ,-0.5 ,-0.5 ,-0.5 ,0.5, -0.5, 0.5 ,-0.5, -0.5, 0.5 ,0.5 ,-0.5] })  
	ri.Patch( "bilinear",{ "P" :  [-0.5 ,-0.5 ,-0.5 ,-0.5, 0.5 ,-0.5 ,-0.5 ,-0.5 ,0.5 ,-0.5, 0.5 ,0.5] })  
	ri.Patch( "bilinear",{ "P" :  [0.5 ,-0.5 ,-0.5 ,0.5 ,0.5 ,-0.5 ,0.5 ,-0.5 ,0.5 ,0.5 ,0.5, 0.5] })     
	ri.Patch( "bilinear",{ "P" :  [0.5, -0.5, 0.5 ,0.5 ,-0.5, -0.5, -0.5 ,-0.5 ,0.5, -0.5 ,-0.5, -0.5] })  
	ri.Patch( "bilinear",{ "P" :  [0.5, 0.5, 0.5 ,0.5 ,0.5, -0.5, -0.5 ,0.5 ,0.5 ,-0.5 ,0.5 ,-0.5] })
	ri.TransformEnd()
	
	ri.TransformBegin()
	ri.Translate( 0.5, -1.0, -1.5)
	ri.Scale (0.2 ,0.2 ,0.2)
	ri.Rotate (-90, 1 ,0 ,0)
	ri.Rotate (55, 0, 0, 1)
	ri.Geometry ("teapot")
	ri.TransformEnd()
	
	ri.TransformBegin()
	ri.Translate( 0, -0.7, 0)
	ri.Scale( 0.2, 0.2, 0.2)
	ri.Rotate( -90, 1 ,0 ,0)
	ri.Rotate( 55, 0, 0, 1)
	ri.Geometry( "teapot")
	ri.TransformEnd()
	ri.TransformBegin()
	
	ri.Translate( 1.3, -0.5 ,.2)
	ri.Rotate( 90, 1, 0, 0)
	ri.Scale( 0.2, 0.2, 1.4)
	ri.Cylinder( 1, -0.5, 0.5, 360) 
	ri.TransformEnd()
	
	ri.TransformBegin()
	
	ri.Translate( 1.3, 0.2, .2)
	ri.Rotate( 90, 1 ,0 ,0)
	ri.Scale( 0.2, 0.2, 2)
	ri.Disk( 0, 1 ,360)
	ri.TransformEnd()
	
	
	
	random.seed(25)
	face=[-0.1,-1,-3, 0.1,-1,-3,-0.1,-1,3, 0.1,-1,3]
	plank=-5.0
	
	ri.AttributeBegin()
	while (plank <=5.0) :
		ri.TransformBegin()
		ri.Color([random.uniform(0.35,0.4),random.uniform(0.1,0.025),0])
		c0=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		c1=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		ri.Surface("wood",{"Ks":[0.1],"point c0":c0,"point c1":c1,"float grain":random.randint(2,20)})
		ri.Translate(plank,0,0)
		ri.Patch("bilinear",{'P':face})
		ri.TransformEnd()
		plank=plank+0.206
	ri.AttributeEnd()

	
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

Pl1=[3.2,-0.6,-2.5]
Pl2=[3.2,0.6,-2.5]
Pl3=[3.0,-0.6,2.0]
Pl4=[3.0,0.6,2.0]



To=[0,0,0]
coneAngle=0.4

SpotName="Spot1"
ShadowPass(ri,SpotName,Pl1,To,coneAngle,Scene)

Spot2Name="Spot2"
ShadowPass(ri,Spot2Name,Pl2,To,coneAngle,Scene)

Spot3Name="Spot3"
ShadowPass(ri,Spot3Name,Pl3,To,coneAngle,Scene)

Spot4Name="Spot4"
ShadowPass(ri,Spot4Name,Pl4,To,coneAngle,Scene)

filename = "AreaLight.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)
ri.Clipping(0.1,20)

# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
ri.Declare("AreaLight" ,"string")

ri.Declare("Ambient" ,"string")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("ShadowSpot.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 

# top view
#ri.Translate(0,0,6)
#ri.Rotate(-90,1,0,0)
#close 
ri.Translate( 0 ,0.0, 5)
ri.Rotate (-10 ,1, 0 ,0)
ri.Rotate( 35 ,0 ,1 ,0)

"""
#normal view
ri.Translate(0,0,4)
"""
# now we start our world
ri.WorldBegin()



ri.LightSource ("ambientlight",{ri.HANDLEID: "Ambient","intensity" :[0.05]}) 

maplist="%s.shad,%s.shad,%s.shad,%s.shad" %(SpotName,Spot2Name,Spot3Name,Spot4Name)
print maplist
# changing shadowbias will give different effects
# 0.02 Pencil Like drawing
# 0.05 smooth
ri.LightSource( "arealight", {ri.HANDLEID:"AreaLight",
				"float intensity" : [3],
				"string maplist" :[maplist], 
				"point Pl1" : Pl1,
				"point Pl2" : Pl2,  
				"point Pl3" : Pl3,  
				"point Pl4" : Pl4,  
				"float gapBias" : [0.3],
				"float shadowBias" : [0.05],
				"float numsamples" : [32] } )

ri.AttributeBegin()
ri.Illuminate("AreaLight",0)
ri.Surface("defaultsurface")
#ri.Opacity([0.5,0.5,0.5])
data=Pl1+Pl2+Pl3+Pl4
#ri.Patch( "bilinear",{ "P" : data })      
ri.AttributeEnd()
Scene(ri)

ri.WorldEnd()

# and finally end the rib file
ri.End()
