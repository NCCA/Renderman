## change shader binding
# Normal Camera
cam=''

cameras={}
cameras['Top']=[Vec4(0,5,0),Vec4(0,0,0),Vec4(0,0,1),40]
cameras['Normal']=[Vec4(0,1.4,2.8),Vec4(0,0,0),Vec4(0,1,0),50]
cameras['Original']=(Vec4(-0.2,0.2,2.5),Vec4(0,0,0),Vec4(0,1,0),65)
if cameras.get(cam) != None :
    ri.EditBegin('option')
    print "moving Camera"
    # Simple translate for our camera
    camParams=cameras.get(cam)
    ri.Projection(ri.PERSPECTIVE,{ri.FOV:[camParams[3]]})
    cam=Camera(camParams[0],camParams[1],camParams[2])
    cam.place(ri)
    ri.Camera( "world")
    ri.EditEnd() 
    

checkAndCompileShader('swirl')

editName='sceneObject'
ri.EditBegin( 'attribute',
{
     'string scopename'  : [editName]
 
})
print "add pattern"

ri.Pattern('swirl','swirl',
{
    'float repeatU' : [5],
    'float repeatV' : [5]
})

ri.Pattern('PxrVoronoise','voronoise2',
{
	'int surfacePosition' : [0], 
	'reference float frequency' : ['swirl:resultF'], 
	'reference int octaves' : ['swirl:resultF'], 
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
