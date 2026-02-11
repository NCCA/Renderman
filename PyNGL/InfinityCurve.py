#!/usr/bin/env -S uv run --script
import math

import numpy as np
import prman
from ncca.ngl import Mat4, PrimData, Transform, Vec3, prim_data_to_ri_points_polygons, renderman_look_at


def infinity_cove(
    width,
    depth,
    height,
    radius,
    width_divs=20,
    depth_divs=20,
    curve_divs=16,
    height_divs=20,
):
    """
    Generate an infinity cove mesh suitable for ri.PointPolygons using numpy.

    Returns:
        None (directly calls ri.PointsPolygons)
    """
    # Clamp radius so it fits
    radius = min(radius, depth, height)
    half_w = width * 0.5

    # --- Build Z profile (depth direction) using numpy ---

    # 1. Floor section (flat)
    flat_depth = depth - radius
    floor_t = np.linspace(0, 1, depth_divs + 1)
    floor_z = -flat_depth * (1 - floor_t)
    floor_y = np.zeros_like(floor_z)

    # 2. Curve (quarter circle)
    curve_t = np.linspace(0, 1, curve_divs + 1)[1:]  # Exclude start to avoid duplication
    curve_angle = curve_t * (np.pi / 2.0)
    curve_z = -radius * np.cos(curve_angle)
    curve_y = radius * np.sin(curve_angle)

    # 3. Wall section (vertical)
    wall_height = height - radius
    wall_t = np.linspace(0, 1, height_divs + 1)[1:]  # Exclude start
    wall_z = np.zeros_like(wall_t)
    wall_y = radius + wall_height * wall_t

    # Combine profiles
    profile_z = np.concatenate([floor_z, curve_z, wall_z])
    profile_y = np.concatenate([floor_y, curve_y, wall_y])
    z_profile = np.vstack([profile_z, profile_y]).T

    rows = len(z_profile)
    cols = width_divs + 1

    # --- Generate points grid using numpy ---
    x_coords = np.linspace(-half_w, half_w, cols)
    # Tile the Z and Y profiles 'cols' times to create the grid
    points = np.zeros((rows * cols, 3), dtype=np.float32)
    points[:, 0] = np.tile(x_coords, rows)
    points[:, 1] = np.repeat(z_profile[:, 1], cols)
    points[:, 2] = np.repeat(z_profile[:, 0], cols)
    # Negate X and Z for 180 degree rotation in Y
    points[:, 0] *= -1
    points[:, 2] *= -1
    # --- Build quad faces using numpy ---
    r = np.arange(rows - 1)
    c = np.arange(width_divs)
    R, C = np.meshgrid(r, c, indexing="ij")

    v0 = R * cols + C
    v1 = v0 + 1
    v2 = (R + 1) * cols + C + 1
    v3 = (R + 1) * cols + C

    # reverse vertex order to flip normals
    verts = np.vstack([v0.ravel(), v3.ravel(), v2.ravel(), v1.ravel()]).T.flatten()
    nverts = np.full((rows - 1) * width_divs, 4, dtype=int).tolist()

    # Flatten point list for RenderMan
    P = points.flatten().tolist()
    # output to stream
    ri.PointsPolygons(nverts, verts.tolist(), {"P": P})


def quarter_cylinder_cove(
    width,
    radius,
    width_divs=20,
    curve_divs=32,
):
    """
    Generate a quarter cylinder cove mesh using numpy.
    """
    half_w = width * 0.5
    cols = width_divs + 1
    rows = curve_divs + 1

    # Create grid of u, v parameters
    u = np.linspace(0, 1, cols)
    v = np.linspace(0, 1, rows)
    U, V = np.meshgrid(u, v)

    # Calculate points from parameters
    X = half_w - U * width
    angle = V * (np.pi / 2.0)
    Y = radius * (1 - np.cos(angle))
    Z = radius * (1 - np.sin(angle))

    # Reshape points into a (N, 3) array
    points = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

    # --- Build quad faces using numpy ---
    r = np.arange(rows - 1)
    c = np.arange(width_divs)
    R, C = np.meshgrid(r, c, indexing="""ij""")

    v0 = R * cols + C
    v1 = v0 + 1
    v2 = (R + 1) * cols + C + 1
    v3 = (R + 1) * cols + C

    # reverse vertex order to flip normals
    verts = np.vstack([v0.ravel(), v3.ravel(), v2.ravel(), v1.ravel()]).T.flatten()
    nverts = np.full((rows - 1) * width_divs, 4, dtype=int).tolist()

    P = points.flatten().tolist()
    ri.PointsPolygons(nverts, verts.tolist(), {"P": P})


# Example usage and visualization
if __name__ == "__main__":
    # Generate the infinity curve mesh

    # Example RenderMan usage (commented out as it requires prman module)

    ri = prman.Ri()
    ri.Begin("__render")

    for frame in range(0, 360, 10):
        ri.Display(f"infinity_curve.{frame:04d}.exr", "it", "rgba")
        ri.FrameBegin(frame)
        ri.Format(1024, 720, 1)
        ri.Projection(ri.PERSPECTIVE, {ri.FOV: [55]})

        look = renderman_look_at(Vec3(0.0, 3, 10), Vec3(0, 0, 0), Vec3(0, 1, 0))
        ri.Identity()
        ri.Transform(look.to_list())

        ri.WorldBegin()

        # print(npolys, nvertices, points)
        ri.TransformBegin()
        ri.Rotate(frame, 0, 1, 0)
        ri.TransformBegin()
        ri.Translate(-2, 0, 0)
        infinity_cove(width=4, depth=4, height=10, radius=2)
        ri.TransformEnd()
        ri.TransformBegin()
        ri.Translate(2, 0, 0)
        quarter_cylinder_cove(width=4, radius=4, width_divs=200, curve_divs=200)
        ri.TransformEnd()
        ri.TransformEnd()
        ri.WorldEnd()
        ri.FrameEnd()
    ri.End()
