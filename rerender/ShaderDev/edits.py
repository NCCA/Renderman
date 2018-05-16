## change shader binding
"""
ri.EditBegin('option')
print "moving Camera"
# Simple translate for our camera
ri.Projection(ri.PERSPECTIVE,{ri.FOV:[40]})
cam=Camera(Vec4(1,1.4,5.8),Vec4(0,0,0),Vec4(0,1,0))
cam.place(ri)
ri.Camera( "world")

ri.EditEnd() 

"""
editName='sceneObject'
ri.EditBegin( 'attribute',
{
     'string scopename'  : [editName]
 
})
print "add pattern"
ri.Pattern('PxrVoronoise','voronoise2',
{
	'int surfacePosition' : [0], 
	'float frequency' : [22.0], 
	'int octaves' : [20], 
	'float gain' : [0.5],   
	'float lacunarity' : [12.0], 
	'float jitter' : [.2], 
	'float smoothness' : [1.0], 
	'int turbulent' : [1],

})
#ri.EditEnd() 

## bxdf parameter edit for the floor
#editName='sceneObject'
print 'change all of the pxrsurface instances' 
# ri.EditBegin( 'attribute',
# {
#   'string scopename'  : [editName]
# }) 


ri.Bxdf('PxrSurface', 'plastic',
{
  'reference color diffuseColor' : ['voronoise2:resultRGB'],
  'float diffuseGain' : [1.0], 
  'int diffuseDoubleSided' : [1],
})
ri.EditEnd()
