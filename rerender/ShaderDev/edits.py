## change shader binding
# Normal Camera
cam='Default'
if cam == 'Normal' :
    ri.EditBegin('option')
    print "moving Camera"
    # Simple translate for our camera
    ri.Projection(ri.PERSPECTIVE,{ri.FOV:[40]})
    cam=Camera(Vec4(0,1.4,2.8),Vec4(0,0,0),Vec4(0,1,0))
    cam.place(ri)
    ri.Camera( "world")
    ri.EditEnd() 
elif cam == 'Top' :
#Top Camera
    ri.EditBegin('option')
    print "moving Camera"
    # Simple translate for our camera
    ri.Projection(ri.PERSPECTIVE,{ri.FOV:[50]})
    cam=Camera(Vec4(0,2.4,0),Vec4(0,0,0),Vec4(0,0,1))
    cam.place(ri)
    ri.Camera( "world")
    ri.EditEnd() 

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
	'int octaves' : [2], 
	'float gain' : [2],   
	'float lacunarity' : [9.0], 
	'float jitter' : [.2], 
	'float smoothness' : [1.0], 
	'int turbulent' : [1],

})


ri.Bxdf('PxrSurface', 'plastic',
{
  'reference color diffuseColor' : ['voronoise2:resultRGB'],
  'float diffuseGain' : [1.0], 
  'int diffuseDoubleSided' : [1],
})
ri.EditEnd()
