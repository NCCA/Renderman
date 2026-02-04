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


# Grab an instance of the rman ctl module (bit like ri in the old API)
rictl = rman.RiCtl.Get()
rictl.PRManBegin(sys.argv)

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

# Set scene options
options = rman.Types.RtParamList()
options.SetString(rman.Tokens.Rix.k_bucket_order, "circle")
options.SetIntegerArray(rman.Tokens.Rix.k_Ri_FormatResolution, [1024, 1024], 2)
options.SetFloat(rman.Tokens.Rix.k_Ri_FormatPixelAspectRatio, 1.0)
options.SetFloat(rman.Tokens.Rix.k_ShadingRate, 1.0)
options.SetFloat(rman.Tokens.Rix.k_Ri_PixelVariance, 0.1)
scene.SetOptions(options)

# Create a simple checker bxdf
material = scene.CreateMaterial(None)
manifold = rman.scenegraph.Shader("Pattern", "PxrManifold2D", "manifold")
manifold.params.SetFloat("scaleS", 4)
manifold.params.SetFloat("scaleT", 2)
checker = rman.scenegraph.Shader("Pattern", "PxrChecker", "checker")
checker.params.SetColor("colorA", (1, 1, 0))
checker.params.SetColor("colorB", (0, 1, 1))
checker.params.SetStructReference("manifold", "manifold:result")
diffuse = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "diffuse")
diffuse.params.SetColorReference("diffuseColor", "checker:resultRGB")
bxdf = [manifold, checker, diffuse]
material.SetBxdf(bxdf)
# Name of Quadric and translation
quadrics = [
    ("Ri:Sphere", (-2.0, 2.0, 0.0)),
    ("Ri:Cone", (0.0, 2.0, 0.0)),
    ("Ri:Cylinder", (2.0, 2.0, 0.0)),
    ("Ri:Hyperboloid", (-2.0, 0.0, 0.0)),
    ("Ri:Paraboloid", (0.0, 0.0, 0.0)),
    ("Ri:Disk", (2.0, 0.0, 0.0)),
    ("Ri:Torus", (0.0, -2.0, 0.0)),
]
for q in quadrics:
    quadric = scene.CreateQuadric(q[0])
    quadric.SetGeometry(q[0])
    quadric.SetMaterial(material)
    transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
    transform.Translate(q[1][0], q[1][1], q[1][2])
    transform.Rotate(-90, 1, 0, 0)
    quadric.SetTransform(transform)
    scene.Root().AddChild(quadric)

# Create render camera and parent under a group
cameraGroup = scene.CreateGroup("cameraGroup")
scene.Root().AddChild(cameraGroup)
camera = scene.CreateCamera("camera")
proj = rman.scenegraph.Shader("Projection", "PxrPerspective", "proj")
proj.params.SetFloat(rman.Tokens.Rix.k_fov, 35)
camera.SetProjection(proj)
transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
transform.Translate(0, 0, -15)
camera.SetTransform(transform)
camera.SetRenderable(True)
cameraGroup.AddChild(camera)

# Render the scene live and asynchronous,
# in this case the render time is given by the sleep
# increasing this will give better quality
scene.Render("prman -live")
time.sleep(0.2)
for i in range(1, int(360 / 5)):
    # Perform a scene edit inside an edit block
    with rman.scenegraph.ScopedEdit(scene):
        transform = rman.Types.RtMatrix4x4(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
        transform.Rotate(5 * i, 0, 1, 0)
        cameraGroup.SetTransform(transform)
    time.sleep(0.5)
# Stop the render
scene.Stop()
# Delete the scene
sgmngr.DeleteScene(scene)

rictl.PRManEnd()
