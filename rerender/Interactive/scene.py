

def drawScene(ri,zpos=0,yoffset=0,ident='') :
  
  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'%s:torus' %(ident)})
  ri.TransformBegin()
  ri.Translate(-1.7,0.5+yoffset,zpos+0.1)
  ri.Rotate(45,0,1,0)
  ri.Scale( 0.2, 0.2, 0.2) 
  ri.Torus(1.00,0.5,0,360,360)
  ri.TransformEnd()
  ri.AttributeEnd()


  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'%s:teapot'%(ident)})
  ri.TransformBegin()
  ri.Translate(-1,yoffset,zpos)
  ri.Rotate( -90, 1 ,0 ,0)
  ri.Scale( 0.15, 0.15, 0.15) 
  ri.Geometry('teapot')
  ri.TransformEnd()
  ri.AttributeEnd()

  
  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'%s:sphere'%(ident)})
  ri.TransformBegin()
  ri.Translate(0,0.3+yoffset,zpos)
  ri.Sphere(0.3,-1,1,360)
  ri.TransformEnd()
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.Attribute( 'identifier',{ 'name' :'%s:cube'%(ident)})
  drawCube(ri,x=1.0,y=0.25+yoffset,z=zpos,ry=45.0,sx=0.5,sy=0.5,sz=0.5)
  ri.AttributeEnd()

  ri.AttributeBegin()
  ri.TransformBegin()
  ri.Attribute( 'identifier',{ 'name' :'%sdisk:'%(ident)})
  ri.Translate(1.8,0.5+yoffset,zpos)
  ri.Scale(0.4,0.4,0.4)
  ri.Disk(0,1,360)
  ri.TransformEnd()
  ri.AttributeEnd()



# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
filename='bake.rib' #'launch:prman? -ctrl $ctrlin $ctrlout'
ri.Begin(filename)

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display('rgb.exr', 'it', 'rgba')
ri.Format(1024,720,1)

# setup the raytrace / integrators

ri.Hider( "raytrace",
{
    "int incremental"  : [1],
    "int minsamples" : [1],
    "int maxsamples" : [256] 
})
ri.Integrator( "PxrPathTracer" , "handle",{ "int maxPathLength" : [4]})

ri.ShadingRate(2)
ri.PixelVariance (0)

ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
ri.Option( 'statistics', {'endofframe' : [ 1 ] })
ri.Option('searchpath',
{
'string shader' : ['../../Lecture4Shaders:.:${RMANTREE}/lib/plugins:@'],
'string texture' : ['../../Lecture4Shaders:.:${RMANTREE}/lib/plugins:@']  
})
ri.Projection(ri.PERSPECTIVE,{ri.FOV:[65]})

# Simple translate for our camera
cam=Camera(Vec4(-0.2,1.5,4.5),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)


# now we start our world
ri.WorldBegin()

#######################################################################
#Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Attribute( 'identifier',{ 'name' :'domeLight'})
ri.Declare('domeLight' ,'string')
#ri.Rotate(45,0,1,0)
ri.Rotate(-90,1,0,0)
#ri.Rotate(100,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
        'string lightColorMap'  : 'Env_StinsonBeach_1350PM_2k.17.tex'
})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################

ri.AttributeBegin()
ri.Bxdf('PxrSurface', 'plastic1',
{
'color diffuseColor' : [0.8,0.8,0.8],
'int diffuseDoubleSided' : [1]

})
drawScene(ri,zpos=0,ident='row0')
ri.AttributeEnd()

ri.AttributeBegin()
ri.Bxdf( 'PxrDisney','Disney1', 
{ 
'color baseColor' : [0.8,0.8,0.8] ,
})
drawScene(ri,zpos=1,ident='row1')
ri.AttributeEnd()

ri.AttributeBegin()
ri.Bxdf('PxrSurface', 'plastic2',
{
'color diffuseColor' : [0.8,0.8,0.8],
'int diffuseDoubleSided' : [1],
'__instanceid' : ['plastic2']

})
drawScene(ri,zpos=2,ident='row2')
ri.AttributeEnd()


ri.AttributeBegin()
ri.Pattern('uvshader','uvshader')
ri.Bxdf('PxrDiffuse', 'uv', 
{ 
'reference color diffuseColor' : ['uvshader:resultRGB']
})
drawScene(ri,zpos=-1,yoffset=0.4,ident='uvrow')
ri.AttributeEnd()

ri.AttributeBegin()
# floor
ri.Bxdf('PxrDiffuse', 'white', 
{ 
'color diffuseColor' : [0.8,0.8,0.8]
})
ri.Attribute( 'identifier',{ 'name' :'floor'})
ri.TransformBegin()
s=5.0
face=[-s,0,-s, s,0,-s,-s,0,s, s,0,s]
ri.Patch('bilinear',{'P':face})
ri.TransformEnd()
ri.AttributeEnd()


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()



