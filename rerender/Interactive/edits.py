## change shader binding
ri.EditBegin('null')
ri.EditEnd()


editName='row1:torus'
ri.EditBegin( 'attribute' ,
{
    'string scopename'  : [editName]
})
ri.Bxdf('PxrSurface' ,'PxrSurface1',
{
    'float diffuseGain' : [1.0],
    'color diffuseColor' : [1 ,2 ,0],
    # 'color specularFaceColor' : [0, 1 ,1],
    # 'float reflectionGain' : [1.0],
    'string __instanceid' : ['row1:torus']
})
ri.EditEnd()

## bxdf parameter edit for the floor
editName='floor'
ri.EditBegin( 'instance',
{
})

ri.Bxdf('PxrDiffuse', 'white', 
{ 
'color diffuseColor' : [1,1.0,1.0],
'string __instanceid' : [editName]
})
ri.EditEnd()


## bxdf parameter edit for the floor
editName='row2:teapot'
ri.EditBegin( 'instance',
{
  'string scopename'  : [editName]
})

ri.Bxdf('PxrSurface', 'plastic2',
{
'color diffuseColor' : [0.2,0.0,1.0],
'int diffuseDoubleSided' : [1],
'string __instanceid' : [editName]
})
ri.EditEnd()

## move light
# ri.EditBegin( 'attribute',
# { 
#     'string scopename' : ['domeLight']
# })
# ri.Identity()
# ri.Rotate(-90,1,0,0)
# ri.Rotate(-100,0,0,1)
# ri.EditEnd()



