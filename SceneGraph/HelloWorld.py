#!/usr/bin/env rmanpy3

import sys
import os
# Find pythonbindings directory and append python path
RMANTREE = os.getenv("RMANTREE")
assert os.path.isdir(RMANTREE), "RMANTREE is invalid"
PYTHONBINDINGS = os.path.abspath(os.path.join(RMANTREE, "bin", "pythonbindings"))
if PYTHONBINDINGS not in sys.path:
    sys.path.append(PYTHONBINDINGS)

# Now import rman modules
import rman


if __name__ == "__main__":

    # Wrap the RenderMan part of the process in PRManBegin/End
    rictl = rman.RiCtl.Get()
    rictl.PRManBegin(sys.argv)

    stats = rman.Stats.AddSession("sphere test")


    # Acquire scene graph interface and check version
    sgmngr = rman.scenegraph.Get()
    config = rman.Types.RtParamList()
    renderConfig = rman.Types.RtParamList()
    stats = rman.Stats.AddSession("Statistics Session")
    scene = sgmngr.CreateScene(config, renderConfig, stats)

    # Set scene options
    options = rman.Types.RtParamList()
    options.SetString(rman.Tokens.Rix.k_bucket_order, "circle")
    options.SetIntegerArray(rman.Tokens.Rix.k_Ri_FormatResolution, [512, 512], 2)
    options.SetFloat(rman.Tokens.Rix.k_Ri_FormatPixelAspectRatio, 1.0)
    scene.SetOptions(options)

    # Create a simple checker bxdf
    material = scene.CreateMaterial(None)
    diffuse = rman.scenegraph.Shader("Bxdf", "PxrDiffuse", "diffuse")
    #diffuse.params.SetColorReference("diffuseColor", "[1,0,0]")
    diffuse.params.SetColor("diffuseColor", (1.0, 0.0, 0.0))

    bxdf = [diffuse]
    material.SetBxdf(bxdf)

    # Create a sphere
    sphere = scene.CreateQuadric("sphere")
    sphere.SetMaterial(material)
    transform = rman.Types.RtMatrix4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    transform.Rotate(-90, 1, 0, 0)
    sphere.SetTransform(transform)
    scene.Root().AddChild(sphere)

    # Create render camera and parent under a group
    cameraGroup = scene.CreateGroup("cameraGroup")
    scene.Root().AddChild(cameraGroup)
    camera = scene.CreateCamera("camera")
    proj = rman.scenegraph.Shader("Projection", "PxrPerspective", "proj")
    proj.params.SetFloat(rman.Tokens.Rix.k_fov, 35)
    camera.SetProjection(proj)
    transform = rman.Types.RtMatrix4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    transform.Translate(0, 0, -5)
    camera.SetTransform(transform)
    camera.SetRenderable(True)
    cameraGroup.AddChild(camera)

    # Render the scene live and asynchronous
    scene.Render("prman ")
    while rictl.GetProgress() !=100 :
        ...


    #time.sleep(0.1)
    
    # for i in range(1, 72):
    #     # Perform a scene edit inside an edit block
    #     with rman.scenegraph.ScopedEdit(scene):
    #         transform = rman.Types.RtMatrix4x4(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    #         transform.Rotate(5 * i, 0, 1, 0)
    #         cameraGroup.SetTransform(transform)
    #     time.sleep(0.1)
    # # Stop the render
    # scene.Stop()

    # Delete the scene
    sgmngr.DeleteScene(scene)

    # Delete the scene
    sgmngr.DeleteScene(scene)


    rictl.PRManEnd()
