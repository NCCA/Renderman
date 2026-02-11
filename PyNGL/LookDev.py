#!/usr/bin/env -S uv run --script
import random
import subprocess
from pathlib import Path

import numpy as np
import prman
import requests
from ncca.ngl import Mat4, PrimData, Transform, Vec3, prim_data_to_ri_points_polygons, renderman_look_at
from tqdm import tqdm

from ColourMatching import render_colorchecker, render_refballs
from InfinityCurve import subdiv_cove_volume

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


def render_floor():
    tx = Transform()
    ri.AttributeBegin()
    ri.Bxdf("PxrDiffuse", "brown", {"color diffuseColor": [0.737, 0.505, 0.37]})
    ri.Attribute("identifier", {"name": "floor"})
    ri.TransformBegin()
    tx.set_position(0, -0.5, 0)
    ri.Transform(tx.get_matrix().to_list())
    subdiv_cove_volume(ri, width=8.0, height=3.0, depth=4.5, crease=1.5)
    ri.TransformEnd()
    ri.AttributeEnd()


def create_light():
    ri.TransformBegin()
    ri.AttributeBegin()

    ri.Declare("domeLight", "string")
    # ri.Light("PxrEnvDayLight", "dayLight", {"int month": 6, "int day": 20, "float hour": 10})

    ri.Rotate(-90, 1, 0, 0)
    ri.Rotate(100, 0, 0, 1)
    ri.Light(
        "PxrDomeLight",
        "domeLight",
        {"float intensity": [0.5], "float exposure": [0.0], "string lightColorMap": "white_studio_02_4k.tex"},
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
    ri.PixelVariance(0.01)
    ri.Display("LookDev.exr", "it", "rgba")
    ri.Format(1024, 720, 1.0)
    # 4K
    # ri.Format(4096, 2160, 1.0)
    ri.Projection(ri.PERSPECTIVE, {ri.FOV: [45]})

    look = renderman_look_at(Vec3(0, 0.5, 4), Vec3(0, 0, 0), Vec3(0, 1, 0))
    ri.Identity()
    ri.Transform(look.to_list())
    # f-stop focalLength focalDistance
    # ri.DepthOfField(22, 1.5, 9)


def main():
    render_to_it = True
    ri.Begin("__render" if render_to_it else "LookDev.rib")
    setup_scene()
    # now we start our world
    ri.WorldBegin()
    create_light()
    # enable transparency and tracing
    ri.Attribute("visibility", {"int transmission": [1]})
    ri.Attribute("trace", {"int maxdiffusedepth": [1], "int maxspeculardepth": [2]})

    # now instance the meshes with random materials
    ri.TransformBegin()
    ri.Translate(0, -0.5, 0)
    ri.Scale(2, 2, 2)
    ri.Rotate(180, 0, 1, 0)
    ri.Bxdf(
        "PxrSurface",
        "plastic",
        {
            "color diffuseColor": [0.9, 0.1, 0.1],
        },
    )
    ri.ReadArchive("YourMeshHere.rib.gz")
    ri.TransformEnd()
    render_refballs(ri, (1.0, -0.25, 1.2), (0.2, 0.2, 0.2))

    ri.TransformBegin()
    tx = Transform()
    tx.set_rotation(-45, 45, 0)
    tx.set_position(-1.2, -0.1, 1.2)
    ri.Transform(tx.get_matrix().to_list())
    render_colorchecker(ri, 0.1, 0.01)
    ri.TransformEnd()

    render_floor()
    ri.WorldEnd()
    # and finally end the rib file
    ri.End()


if __name__ == "__main__":
    HDR_FILE = "white_studio_02_4k.exr"
    URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/4k/white_studio_02_4k.exr"
    check_and_download_hdr(HDR_FILE, URL)
    main()
