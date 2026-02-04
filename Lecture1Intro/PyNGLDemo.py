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

troll_data = PrimData.primitive("bunny")
nvertices, vertices, parameterlist = triangles_to_ri_points_polygons(troll_data)

# FILENAME DISPLAY Type Output format
ri.Display("PyNGL.exr", "it", "rgba")
ri.Format(1024, 720, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: [45]})
look = renderman_look_at(Vec3(0, 7, 32), Vec3(0, 0, 0), Vec3(0, 1, 0))
# # Need to flip y,z for renderman
ri.Identity()
ri.Transform(look.to_list())
# now we start our world
ri.WorldBegin()

tx = Transform()
for x in range(-20, 22, 2):
    for z in range(-20, 22, 2):
        tx.reset()
        tx.set_position(x, 0, z)
        tx.set_rotation(0, random.randint(0, 360), 0)
        tx.set_scale(0.2, 0.2, 0.2)
        ri.TransformBegin()
        ri.Transform(tx.get_matrix().to_list())
        # ri.Geometry("teapot
        ri.PointsPolygons(nvertices, vertices, parameterlist)

        ri.TransformEnd()
ri.WorldEnd()
# and finally end the rib file
ri.End()
