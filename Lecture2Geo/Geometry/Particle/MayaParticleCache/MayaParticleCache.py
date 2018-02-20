#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import os,sys,time,random
# import the python renderman library
import prman


def OpenCacheFile(ri,FileName) :
	print "reading ",FileName
	ip=open(FileName,'r')
	#grab the data as lines
	data=ip.readlines()
	# for each line check for one of our tokens
	index=0
	points=[]
	for line in data :
		tokens=line.split()
		index+=1
		if len(tokens) > 0 :
			if(tokens[0] == "NUMBER_OF_PARTICLES:" ) :
				NumParticles=int(tokens[1])
				print "NumberofParticles to process ",NumParticles
			elif(tokens[0]=="BEGIN") :
				#so we only have data now grab it all dangerous but works
				for i in range(index,len(data) ):
					points.append(data[i].split())
				break
	p=[]
	w=[]
	app=p.append
	wa=w.append
	for i in range(0,len(points)) :
			for x in range(0,len(points[i])) :
				app(float(points[i][x]))
			wa(0.1)
				
	ri.Points({ri.P:p,"varying float width":w})
	
	
ri = prman.Ri() # create an instance of the RenderMan interface

ri.Option("rib", {"string asciistyle": "indented"})
PDAdir="./pda/"


FileNames=os.listdir(PDAdir)

frame=0
for Files in FileNames :
	if (Files.endswith('.pda')  ):
		print "creating rib file for",Files
		
		filename = "Particle.%03d.rib" %(frame)
		# this is the begining of the rib archive generation we can only
		# make RI calls after this function else we get a core dump
		ri.Begin(filename)

		# now we add the display element using the usual elements
		# FILENAME DISPLAY Type Output format
		ri.Display("Particle.%03d.exr" %(frame), "file", "rgba")
		# Specify PAL resolution 1:1 pixel Aspect ratio
		ri.Format(720,575,1)
		# now set the projection to perspective
		ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
		# now we start our world
		ri.WorldBegin()
		
		ri.Translate(0,-2,20)
		ri.Rotate(35,0,1,0)
		ri.Bxdf( 'PxrDiffuse','bxdf', 
		{
			'color diffuseColor' : [0,0,0.8]
		})		
		OpenCacheFile(ri,PDAdir+Files)

		ri.WorldEnd()
		# and finally end the rib file
		frame+=1
		ri.End()
