#!/usr/bin/env -S uv run --script
import random
import subprocess
from pathlib import Path

import numpy as np
import prman
import requests
from ncca.ngl import Mat4, PrimData, Transform, Vec3, prim_data_to_ri_points_polygons, renderman_look_at
from tqdm import tqdm


def check_and_download_hdr(filename: str, url: str):
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


def random_material(ri, colour):
    materials = [
        lambda: ri.Bxdf("LamaConductor", "conductor", {"color tint": colour}),
        # lambda: ri.Bxdf("LamaDielectric", "id", {"color reflectionTint": colour}),
        lambda: ri.Bxdf("PxrSurface", "pxrsurface", {"color diffuseColor": colour}),
        lambda: ri.Bxdf("PxrDisney", "id", {"color baseColor": colour}),
        lambda: ri.Bxdf("LamaDiffuse", "id", {"color color": colour, "color diffuseColor": colour}),
    ]
    random.choice(materials)()


def main():
    ri = prman.Ri()  # create an instance of the RenderMan interface

    filename = "__render"
    ri.Begin(filename)
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
            "int allowCaustics": 0,
            "int risPathGuiding": 1,
        },
    )

    ri.Option("hider", {"int minsamples": 4, "int maxsamples": 1024})
    ri.Option("statistics", {"filename": ["stats.txt"]})
    ri.Option("statistics", {"endofframe": [1]})

    ri.ShadingRate(0.05)
    ri.PixelVariance(0.0)
    # FILENAME DISPLAY Type Output format
    ri.Display("PyNGL.exr", "it", "rgba")
    ri.Format(1024, 720, 1.2)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: [55]})

    look = renderman_look_at(Vec3(0.5, 3, 58), Vec3(0, 0, 0), Vec3(0, 1, 0))
    ri.Identity()
    ri.Transform(look.to_list())
    # f-stop focalLength focalDistance
    # ri.DepthOfField(22, 1.5, 9)

    # now we start our world
    ri.WorldBegin()
    models = []
    random.seed(1234)

    big_tx = Transform()
    big_tx.set_scale(0.2, 0.2, 0.2)
    unit_tx = Transform()
    unit_tx.set_position(0, 1.0, 0)
    unit_tx.set_scale(2, 2, 2)
    platonic_tx = Transform()
    platonic_tx.set_position(0, 1, 0)
    meshes = [
        ("bunny", big_tx),
        ("buddah", big_tx),
        ("dragon", big_tx),
        ("troll", unit_tx),
        ("teapot", unit_tx),
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
    models.append(id)
    ri.ObjectEnd()

    #######################################################################
    # Lighting We need geo to emit light
    #######################################################################
    ri.TransformBegin()
    ri.AttributeBegin()
    ri.Declare("domeLight", "string")
    # ri.Rotate(45, 0, 1, 0)
    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(100, 0, 0, 1)
    ri.Light(
        "PxrDomeLight",
        "domeLight",
        {"float intensity": [0.5], "float exposure": [0.0], "string lightColorMap": "autumn_hilly_field_8k.tex"},
    )
    ri.AttributeEnd()
    ri.TransformEnd()
    #######################################################################

    tx = Transform()
    for x in range(-40, 42, 3):
        for z in range(-50, 62, 3):
            tx.reset()
            tx.set_position(x, 0, z)
            tx.set_rotation(0, -90 + random.randint(-20, 20), 0)
            ri.TransformBegin()
            ri.Transform(tx.get_matrix().to_list())
            colour = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
            ri.Attribute("visibility", {"int transmission": [1]})
            ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [2]})

            random_material(ri, colour)

            ri.ObjectInstance(random.choice(models))

            ri.TransformEnd()

    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "white", {"color diffuseColor": [0.8, 0.8, 0.8]})
    ri.Attribute("identifier", {"name": "floor"})
    ri.TransformBegin()
    tx.reset()
    tx.set_position(0, -0.5, 0)
    ri.Transform(tx.get_matrix().to_list())
    ri.ObjectInstance(plane)
    ri.TransformEnd()
    ri.AttributeEnd()

    ri.WorldEnd()
    # and finally end the rib file
    ri.End()


if __name__ == "__main__":
    HDR_FILE = "autumn_hilly_field_8k.exr"
    URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/8k/autumn_hilly_field_8k.exr"
    check_and_download_hdr(HDR_FILE, URL)
    main()
