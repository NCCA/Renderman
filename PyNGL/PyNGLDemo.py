#!/usr/bin/env -S uv run --script
import random

import numpy as np
import prman
from ncca.ngl import Mat4, PrimData, Transform, Vec3, renderman_look_at


def triangles_to_ri_points_polygons(triangles):
    """
    Convert a packed numpy array of triangles to RenderMan PointsPolygons format.

    Parameters
    ----------
    triangles : np.ndarray
        Array of shape (n_vertices, 8) where each row is: x, y, z, nx, ny, nz, u, v
        n_vertices must be divisible by 3 (since we have triangles)

    Returns
    -------
    tuple
        (nvertices, vertices, parameterlist)
        - nvertices: list of vertex counts per polygon (all 3 for triangles)
        - vertices: flat list of vertex indices
        - parameterlist: dict with 'P', 'N', 'st' arrays for RenderMan
    """
    # Ensure it's a 2D array
    if triangles.ndim == 1:
        # If completely flat, reshape to (n_verts, 8)
        if len(triangles) % 8 != 0:
            raise ValueError("1D array length must be divisible by 8")
        triangles = triangles.reshape(-1, 8)

    n_verts = triangles.shape[0]
    if n_verts % 3 != 0:
        raise ValueError("Number of vertices must be divisible by 3")

    n_triangles = n_verts // 3

    # Extract components from each row
    positions = triangles[:, 0:3]  # (n_verts, 3) - x, y, z
    normals = triangles[:, 3:6]  # (n_verts, 3) - nx, ny, nz
    uvs = triangles[:, 6:8]  # (n_verts, 2) - u, v

    # RenderMan PointsPolygons format
    nvertices = [3] * n_triangles  # Each polygon has 3 vertices
    vertices = list(range(n_verts))  # Sequential vertex indices

    # Parameter list - flatten to 1D arrays as RenderMan expects
    parameterlist = {
        "P": positions.flatten().tolist(),  # Position
        "N": normals.flatten().tolist(),  # Normals
        "st": uvs.flatten().tolist(),  # Texture coordinates
    }

    return nvertices, vertices, parameterlist


ri = prman.Ri()  # create an instance of the RenderMan interface

filename = "__render"
ri.Begin("__render")
ri.Hider("raytrace", {"int incremental": [1]})
ri.Attribute("Ri", {"int Sides": [2]})

# ri.ShadingRate(0.01)
# ri.PixelVariance(0.0001)
ri.Integrator("PxrUnified", "integrator", {})

troll_data = PrimData.primitive("bunny")
nvertices, vertices, parameterlist = triangles_to_ri_points_polygons(troll_data)

models = []
models.append(triangles_to_ri_points_polygons(PrimData.primitive("bunny")))
models.append(triangles_to_ri_points_polygons(PrimData.primitive("buddah")))
models.append(triangles_to_ri_points_polygons(PrimData.primitive("dragon")))

# FILENAME DISPLAY Type Output format
ri.Display("PyNGL.exr", "it", "rgba")
ri.Format(1024 * 2, 720 * 2, 1.2)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: [45]})
look = renderman_look_at(Vec3(0.5, 6, 38), Vec3(0, 0, 0), Vec3(0, 1, 0))
# # Need to flip y,z for renderman
ri.Identity()
ri.Transform(look.to_list())


# now we start our world
ri.WorldBegin()

#######################################################################
# Lighting We need geo to emit light
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("domeLight", "string")
ri.Rotate(45, 0, 1, 0)
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(100, 0, 0, 1)
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "Env_StinsonBeach_1350PM_2k.17.tex"})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################

tx = Transform()
for x in range(-20, 22, 3):
    for z in range(-20, 22, 3):
        tx.reset()
        tx.set_position(x, 0, z)
        tx.set_rotation(0, -90 + random.randint(-20, 20), 0)
        tx.set_scale(0.2, 0.2, 0.2)
        ri.TransformBegin()
        ri.Transform(tx.get_matrix().to_list())
        # ri.Geometry("teapot
        colour = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        # ri.Bxdf("PxrSurface", "plastic", {"color diffuseColor": colour, "int diffuseDoubleSided": [1]})
        ri.Bxdf(
            "LamaConductor",
            "id",
            {
                "color tint": colour,
                "int fresnelMode": [0],
                "color reflectivity": [0.9450, 0.7772, 0.3737],
                "color edgeColor": [0.7137, 0.7373, 0.4550],
                "color IOR": [0.18, 0.42, 1.37],
                "color extinction": [3.42, 2.35, 1.77],
                "float roughness": [0.1],
                "color shadowColor": [0.0, 0.0, 0.0],
                "float tailMix": [0.0],
                "float tailLength": [0.5],
                "float anisotropy": [0.0],
                "vector anisotropyDirection": [0.0, 0.0, 0.0],
                "float anisotropyRotation": [0.0],
                "int overrideExteriorIOR": [0],
                "float exteriorIOR": [1.0],
                "int edgeColorMode": [0],
                "float energyCompensation": [1.0],
                "int bumpShadowing": [1],
                "float surfaceMollification": [1.0],
                "float motionMollification": [0.0],
                "string lobeName": ["specular"],
                "string matte": [""],
            },
        )

        nvertices, vertices, parameterlist = random.choice(models)

        ri.PointsPolygons(nvertices, vertices, parameterlist)

        ri.TransformEnd()


ri.AttributeBegin()
# floor
# ri.Bxdf(
#     "LamaDiffuse",
#     "lammadiffuse",
#     {
#         "color diffuseColor": [0.9, 0.9, 0.9],
#         "float roughness": [0.8],
#         "color shadowColor": [0.0, 0.0, 0.0],
#         "float energyCompensation": [1.0],
#         "int bumpShadowing": [1],
#         "string lobeName": ["diffuse"],
#         "string matte": [""],
#     },
# )
ri.Bxdf("PxrDiffuse", "white", {"color diffuseColor": [0.8, 0.8, 0.8]})
ri.Attribute("identifier", {"name": "floor"})
ri.TransformBegin()
s = 45.0
face = [-s, 0, -s, s, 0, -s, -s, 0, s, s, 0, s]
tx.reset()
tx.set_position(0, 0, 0)
ri.Transform(tx.get_matrix().to_list())
ri.Patch("bilinear", {"P": face})

ri.TransformEnd()
ri.AttributeEnd()


ri.WorldEnd()
# and finally end the rib file
ri.End()
