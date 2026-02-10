#!/usr/bin/env -S uv run --script
import random
import subprocess
from pathlib import Path

import numpy as np
import prman
import requests
from ncca.ngl import Mat4, PrimData, Transform, Vec3, prim_data_to_ri_points_polygons, renderman_look_at
from tqdm import tqdm

# Not ideal be we need to create an instance of the RenderMan interface, this is global and is basically
# the RenderMan interface context. You can have many context if you need them
ri = prman.Ri()  # create an instance of the RenderMan interface


def check_and_download_hdr(filename: str, url: str):
    """
    Check if the HDR file exists, if not download it and convert it to a texture file using txmake.
    Args:
        filename: The name of the HDR file.
        url: The URL to download the HDR file from.

    """
    if not Path(filename).exists():
        print(f"{filename} not present downloading it")
        resp = requests.get(url, stream=True, verify=False)
        total = int(resp.headers.get("content-length", 0))
        with (
            open(filename, "wb") as file,
            tqdm(desc=filename, total=total, unit="iB", unit_scale=True, unit_divisor=1024) as progress_bar,
        ):
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
    tex_file = filename[: filename.find(".")] + ".tex"
    if not Path(tex_file).exists():
        print(f"{tex_file} not present converting it to tex")
        subprocess.run(["txmake", filename, tex_file])
        print("done")


def random_material(colour):
    """
    Generate a random material with the given colour, this outputs directly to the current ri context so much be called
    in the correct place to be effective.

    Args:
        colour (list): A list of three floats representing the RGB colour values.

    Returns:
        None
    """
    materials = [
        lambda: ri.Bxdf("LamaConductor", "conductor", {"color tint": colour}),
        lambda: ri.Bxdf("LamaDielectric", "id", {"color reflectionTint": colour}),
        lambda: ri.Bxdf("PxrSurface", "pxrsurface", {"color diffuseColor": colour}),
        lambda: ri.Bxdf("PxrDisney", "id", {"color baseColor": colour}),
        lambda: ri.Bxdf("LamaDiffuse", "id", {"color color": colour, "color diffuseColor": colour}),
    ]
    random.choice(materials)()


def render_floor(plane):
    tx = Transform()
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "brown", {"color diffuseColor": [0.737, 0.505, 0.37]})
    ri.Attribute("identifier", {"name": "floor"})
    ri.TransformBegin()
    tx.set_position(0, -0.5, 0)
    ri.Transform(tx.get_matrix().to_list())
    ri.ObjectInstance(plane)
    ri.TransformEnd()
    ri.AttributeEnd()


def generate_model_instances():
    """
    Generate model instances for the scene as well as the floor material
    Note that this actually writes the data to the current ri context immediately so this needs to be
    called before any other ObjectInstance calls that refere to these ID's
    Returns:
        models (list): List of model instances (str,Transform)
        plane (str): instance string for the plane
    """
    models = []
    big_tx = Transform()
    big_tx.set_scale(0.2, 0.2, 0.2)
    unit_tx = Transform()
    unit_tx.set_position(0, 1.1, 0)
    unit_tx.set_scale(2, 2, 2)
    teapot_tx = Transform()
    teapot_tx.set_position(0, 1.0, 0)
    teapot_tx.set_scale(2, 2, 2)
    platonic_tx = Transform()
    platonic_tx.set_position(0, 1, 0)
    meshes = [
        ("bunny", big_tx),
        ("buddah", big_tx),
        ("dragon", big_tx),
        ("troll", unit_tx),
        ("teapot", teapot_tx),
        ("icosahedron", platonic_tx),
        ("tetrahedron", platonic_tx),
        ("octahedron", platonic_tx),
        ("dodecahedron", platonic_tx),
    ]
    # generate objects for the scene. They can also have local scales
    for mesh, tx in meshes:
        id = ri.ObjectBegin()
        nvertices, vertices, parameterlist = prim_data_to_ri_points_polygons(PrimData.primitive(mesh))
        ri.TransformBegin()
        ri.Identity()
        ri.Transform(tx.get_matrix().to_list())
        ri.PointsPolygons(nvertices, vertices, parameterlist)
        ri.TransformEnd()
        models.append(id)
        ri.ObjectEnd()

    plane = ri.ObjectBegin()
    nvertices, vertices, parameterlist = prim_data_to_ri_points_polygons(
        PrimData.triangle_plane(180, 180, 1, 1, Vec3(0, 1, 0))
    )
    ri.TransformBegin()
    ri.Translate(0, 0.5, 0)
    ri.PointsPolygons(nvertices, vertices, parameterlist)
    ri.TransformEnd()
    ri.ObjectEnd()
    return models, plane


def create_light():
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(100, 0, 0, 1)
    ri.Light(
        "PxrDomeLight",
        "domeLight",
        {"float intensity": [0.5], "float exposure": [0.0], "string lightColorMap": "autumn_hilly_field_8k.tex"},
    )
    ri.AttributeEnd()
    ri.TransformEnd()


def setup_scene():
    ri.Hider("raytrace", {"int incremental": [1]})
    ri.Attribute("Ri", {"int Sides": [2]})

    ri.PixelFilter("gaussian", 2.0, 2.0)

    ri.Integrator(
        "PxrPathTracer",
        "integrator",
        {
            "int maxIndirectBounces": 10,
            "int rouletteDepth": 4,
            "float rouletteThreshold": 0.2,
            "int clampDepth": 2,
            "string sampleMode": "bxdf",
            "int allowCaustics": 1,
            "int risPathGuiding": 1,
        },
    )

    ri.Option("hider", {"int minsamples": 4, "int maxsamples": 1024})
    ri.Option("statistics", {"filename": ["stats.txt"]})
    ri.Option("statistics", {"endofframe": [1]})

    ri.ShadingRate(0.1)
    ri.PixelVariance(0.001)
    ri.Display("PyNGL.exr", "it", "rgba")
    i.Format(1024, 720, 1.0)
    # 4K
    # ri.Format(4096, 2160, 1.0)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: [55]})

    look = renderman_look_at(Vec3(0.5, 3, 75), Vec3(0, 0, 0), Vec3(0, 1, 0))
    ri.Identity()
    ri.Transform(look.to_list())
    # f-stop focalLength focalDistance
    # ri.DepthOfField(22, 1.5, 9)


def main():
    render_to_it = False
    ri.Begin("__render" if render_to_it else "PyNGLScene.rib")
    setup_scene()
    # now we start our world
    ri.WorldBegin()
    # this returns the id's of the object instances created in the function
    models, plane = generate_model_instances()
    create_light()
    # enable transparency and tracing
    ri.Attribute("visibility", {"int transmission": [1]})
    ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [2]})

    # now instance the meshes with random materials
    tx = Transform()

    for z in range(-50, 62, 3):
        model = random.choice(models)
        for x in range(-40, 42, 3):
            tx.reset()
            tx.set_position(x, 0, z)
            tx.set_rotation(0, -90 + random.randint(-20, 20), 0)
            ri.TransformBegin()
            ri.Transform(tx.get_matrix().to_list())
            ri.AttributeBegin()
            colour = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
            random_material(colour)
            ri.ObjectInstance(model)
            ri.AttributeEnd()
            ri.TransformEnd()

    render_floor(plane)
    ri.WorldEnd()
    # and finally end the rib file
    ri.End()


if __name__ == "__main__":
    HDR_FILE = "autumn_hilly_field_8k.exr"
    URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/8k/autumn_hilly_field_8k.exr"
    check_and_download_hdr(HDR_FILE, URL)
    # good seeds (rabbit front 12434) (teapot 134) (icosahedron 12) (troll 666  )
    random.seed(12434)
    main()
