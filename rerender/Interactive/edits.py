## change shader binding

ri.EditBegin('option')
print "moving Camera"
# Simple translate for our camera
ri.Projection(ri.PERSPECTIVE,{ri.FOV:[75]})
cam=Camera(Vec4(1.2,2.5,4.5),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)
ri.Camera( "world")

ri.EditEnd()


editName='row1:torus'
print 'edit row1:torus shader'
ri.EditBegin( 'attribute' ,
{
    'string scopename'  : [editName]
})
ri.Bxdf('PxrSurface' ,'PxrSurface1',
{
    'float diffuseGain' : [1.0], 
    'color diffuseColor' : [1 ,0 ,1],
    # 'color specularFaceColor' : [0, 1 ,1],
    # 'float reflectionGain' : [1.0],
    'string __instanceid' : ['row1:torus']
})
ri.EditEnd()

## bxdf parameter edit for the floor
editName='floor'
print 'Change colour of floor' 
ri.EditBegin( 'attribute',
{
    'string scopename'  : [editName]
})

ri.Bxdf('PxrDiffuse', 'white', 
{ 
'color diffuseColor' : [0,0.0,1.0],
'string __instanceid' : [editName]
})
ri.EditEnd()


## bxdf parameter edit for the floor
editName='plastic2'
print 'change all of the plastic2 instances'
ri.EditBegin( 'instance',
{
  'string scopename'  : [editName]
})

ri.Bxdf('PxrSurface', 'plastic2',
{
  'color diffuseColor' : [1.0,0.0,0.0],
  'float diffuseGain' : [1.0], 
  'int diffuseDoubleSided' : [1],
  'int specularFresnelMode' : [1], 
  'color specularFaceColor' : [0.2,0.2,0.2], 
  'color specularEdgeColor' : [0,0.2,0], 
  'float specularFresnelShape' : [15.0], 
  'color specularIor' : [1.5,1.5,1.5],
  'string __instanceid' : [editName]
})
ri.EditEnd()

## move light
print 'rotate light'
ri.EditBegin( 'attribute',
{ 
    'string scopename' : ['domeLight']
})
ri.Identity()
ri.Rotate(-90,1,0,0)
ri.Rotate(-100,0,0,1)
ri.EditEnd()



