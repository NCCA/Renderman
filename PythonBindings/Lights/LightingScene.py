#!/usr/bin/env rmanpy3
import sys
import os
import time

# Find pythonbindings directory and append python path
RMANTREE = os.getenv("RMANTREE")
assert os.path.isdir(RMANTREE), "RMANTREE is invalid"
PYTHONBINDINGS = os.path.abspath(os.path.join(RMANTREE, "bin", "pythonbindings"))
if PYTHONBINDINGS not in sys.path:
    sys.path.append(PYTHONBINDINGS)

# Now import rman modules
import rman

Constants = rman.Tokens.Rix


def createSphere(scene, group):
    material = scene.CreateMaterial(None)
    du = rman.scenegraph.Shader("Pattern", "PxrVariable", "du")
    # these get added to the stream one after the other
    du.params.SetString("variable", "du")
    du.params.SetString("type", "float")
    dv = rman.scenegraph.Shader("Pattern", "PxrVariable", "dv")
    dv.params.SetString("variable", "dv")
    dv.params.SetString("type", "float")

    starball = rman.scenegraph.Shader("Pattern", "starBall", "starBall")
    starball.params.SetFloatReference("du", "du:resultR")
    starball.params.SetFloatReference("dv", "dv:resultR")
    surface = rman.scenegraph.Shader("Bxdf", "PxrSurface", "diffuse")
    surface.params.SetColorReference("diffuseColor", "starBall:Cout")
    # this order is important as it specifies how the appear in the rib stream.
    # in this case du,dv feedb into starBall then starball is used for the PxrSurface diffuse
    bxdf = [du, dv, starball, surface]
    material.SetBxdf(bxdf)

    quadric = scene.CreateQuadric("starball")
    quadric.SetGeometry("Ri:Sphere")
    quadric.SetMaterial(material)
    transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
    transform.Translate(0.3, -0.7, 0.3)
    transform.Rotate(-30, 0, 1, 0)
    transform.Rotate(20, 1, 0, 0)
    transform.Scale(0.3, 0.3, 0.3)
    quadric.SetTransform(transform)
    scene.Root().AddChild(quadric)



def buddha(scene,group,ri) :
    #ri.ReadArchive("buddha.zip!buddha.rib",None)
    #Procedural(self, data, bound, sfunc, ffunc)
    white = scene.CreateMaterial(None)
    bxdf = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "white")
    bxdf.params.SetColor("diffuseColor", (0.8, 0.8, 0.8))
    white.SetBxdf(bxdf)
    bound=[-20.5 ,20.5 ,-20.5 ,20.5 ,-20.5 ,20.5]
    ri.Procedural(["teapot.rib"],bound,"ProcDelayedReadArchive",None)
    


def cornellBox(scene, group):

    # Create scene materials: white, red, and green
    white = scene.CreateMaterial(None)
    bxdf = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "white")
    bxdf.params.SetColor("diffuseColor", (0.8, 0.8, 0.8))
    white.SetBxdf(bxdf)
    red = scene.CreateMaterial(None)
    bxdf = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "red")
    bxdf.params.SetColor("diffuseColor", (0.8, 0, 0))
    red.SetBxdf(bxdf)
    green = scene.CreateMaterial(None)
    bxdf = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "green")
    bxdf.params.SetColor("diffuseColor", (0, 0.8, 0))
    green.SetBxdf(bxdf)

    box = [
        ("floor", [-1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1], white),
        ("ceiling", [-1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1], white),
        ("leftWall", [-1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1], red),
        ("rightWall", [1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1], green),
        ("backWall", [-1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1], white),
    ]

    for wall in box:
        mesh = scene.CreateMesh(wall[0])
        mesh.Define(1, 4, 4)
        primvars = mesh.GetPrimVars()

        primvars.SetPointDetail(Constants.k_P, wall[1], "vertex")
        primvars.SetIntegerDetail(Constants.k_Ri_nvertices, [4], "uniform")
        primvars.SetIntegerDetail(Constants.k_Ri_vertices, [0, 1, 2, 3], "facevarying")
        mesh.SetPrimVars(primvars)
        mesh.SetMaterial(wall[2])
        group.AddChild(mesh)


# Grab an instance of the rman ctl module (bit like ri in the old API)
rictl = rman.RiCtl.Get()
rictl.PRManBegin(sys.argv)
riContext = rictl.GetRiCtx()
# Acquire scene graph interface and check version
sgmngr = rman.scenegraph.Get()
if sgmngr.GetVersion() != 3:
    print("wrong version of API")
    sys.exit()

# Create the scene
config = rman.Types.RtParamList()
renderConfig = rman.Types.RtParamList()
statsSession = rman.Stats.AddSession("stats")
scene = sgmngr.CreateScene(config, renderConfig, statsSession)

# Set the scene integrator
integrator = rman.scenegraph.Shader("Integrator", "PxrPathTracer", "integrator")
scene.SetIntegrator(integrator)

# Set scene options
options = rman.Types.RtParamList()
#options.SetString(Constants.k_bucket_order, "circle")
options.SetIntegerArray(Constants.k_Ri_FormatResolution, [1024, 1024], 2)
options.SetFloat(Constants.k_Ri_FormatPixelAspectRatio, 1.0)
options.SetFloat(Constants.k_ShadingRate, 1.0)
options.SetFloat(Constants.k_Ri_PixelVariance, 0.1)


options.SetString(Constants.k_searchpath_archive, "../../Lecture3/assets/:@")
options.SetString(Constants.k_searchpath_shader, "../../Lecture3Lighting/:@")

scene.SetOptions(options)

riContext.ArchiveRecord(Constants.k_comment, "test")

# Create and add the light to the cornell box
light = scene.CreateAnalyticLight("light")
group = scene.CreateGroup("root")
scene.Root().AddChild(group)

rect = rman.scenegraph.Shader("Light", "PxrRectLight", "rect")
rect.params.SetFloat("intensity", 10.0)
light.SetLight(rect)
transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
transform.Translate(0, 1 - 0.05, 0)
transform.Rotate(90, 1, 0, 0)
transform.Scale(0.5, 0.5, 1)

light.SetTransform(transform)
group.AddChild(light)

cornellBox(scene, group)
createSphere(scene, group)
buddha(scene,group,riContext)

# Create render camera and parent under a group
cameraGroup = scene.CreateGroup("cameraGroup")
scene.Root().AddChild(cameraGroup)
camera = scene.CreateCamera("camera")
proj = rman.scenegraph.Shader("Projection", "PxrPerspective", "proj")
proj.params.SetFloat(Constants.k_fov, 39.3)
camera.SetProjection(proj)
transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
transform.Translate(0, 0, -3.9)
camera.SetTransform(transform)
camera.SetRenderable(True)
cameraGroup.AddChild(camera)

# Render the scene (to output driver specified in Display)
# '-live'     | Interactive rendering supporting scene edits
# '-blocking' | Call blocks unitl stopped or converged
scene.Render("prman -blocking")
# if we wish to dump to rib use the following
# scene.Render('rib scene.rib')
# Stop the render
scene.Stop()
# Delete the scene
sgmngr.DeleteScene(scene)

rictl.PRManEnd()
