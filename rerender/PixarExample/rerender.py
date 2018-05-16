#!/usr/bin/python
import prman

ri = prman.Ri() # create an instance of the RenderMan interface

ri.Begin('__render')


ri.Display( "rerender", "it", "rgba")
ri.Hider('raytrace' ,
{
    'int incremental' :[1],
    "int minsamples"  : [1],
    "int maxsamples"  :[4] 
})

ri.PixelVariance(0)
ri.Integrator ("PxrPathTracer", "handle",
{ 
    "int maxPathLength" : [10] 
})	

ri.Option( "rerender", 
{
    "int[2] lodrange" : [0,3]
})

ri.EditWorldBegin( "PxrRectLight.rib" , 
{
"string rerenderer" : "raytrace", 
"int progressive" : [1]
})


for i in range(0,10) :
    ri.EditBegin( "instance",
    { 
    #    "string scopename" : ["teapot_archive"]
    })
    colour=[i/10.0,i/10.0,i/10.0]
    ri.Bxdf("PxrDisney" ,"PxrDisney1",
    {
        "color baseColor" : colour,
        "string __instanceid" : ["teapot_archive"]
    })
    ri.EditEnd()


    # ## bxdf parameter edit
    # ri.EditBegin( "instance")
    # ri.Bxdf( "PxrDisney", "PxrDisney1",
    # { 
    #     "color baseColor" : [1, 1, 0], 
    #     "__instanceid" : ["teapot_archive"]
    # })

    # ri.EditEnd()

    # ## change shader binding
    # ri.EditBegin( "attribute" ,
    # {
    #     "string scopename"  : ["left_wall"]
    # })
    # ri.Bxdf("PxrSurface" ,"PxrSurface1",
    # {
    #     "float diffuseGain" : [0.0],
    #     "color diffuseColor" : [1 ,1 ,1],
    #     "color specularFaceColor" : [1, 1 ,1],
    #     "float reflectionGain" : [1.0],
    #     "string __instanceid" : ["left_wall"]
    # })
    # ri.EditEnd()

    # ## edit light parameter
    # ri.EditBegin( "instance")
    # ri.Light( "PxrRectLight", "Light0",
    # {
    #     "float exposure" : [2], 
    #     "string __instanceid" : ["Light0"]
    # })
    # ri.EditEnd()

    # ## move light
    # ri.EditBegin( "attribute",
    # { 
    #     "string scopename" : ["Light0"]
    # })
    # ri.Translate( 0, 1 ,0)
    # ri.Rotate( 90 ,1 ,0, 0)
    # ri.Scale( 0.5, 0.5, 0.5)
    # ri.Translate( 0, 2, 0)
    # ri.EditEnd()

    # ## add light
    # ri.EditBegin ("attribute")
    # ri.Translate( -0.5, 0.5, 0)
    # ri.Scale( 0.125, 0.125, 0.125)
    # ri.Light( "PxrSphereLight", "Light1",
    # {
    #     "float exposure" : [4],
    #     "string __instanceid" : ["Light1"]

    # })
    # ri.EditEnd()

    # ## mute light
    # ri.EditBegin ("overrideilluminate")
    # ri.Illuminate ("Light0", 0)
    # ri.EditEnd()

    ## move camera
    # ri.EditBegin( "option")
    # ri.Identity()
    # ri.Rotate( i*15, 0 ,1,0)
    # ri.Translate( 0 ,0, 2)
    # ri.Camera ("world")
    # ri.EditEnd()
    print "done edit %d" %(i)

ri.EditWorldEnd()
ri.End()