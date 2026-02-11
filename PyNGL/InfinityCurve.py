#!/usr/bin/env -S uv run --script
import math

import numpy as np
import prman
from ncca.ngl import Mat4, PrimData, Transform, Vec3, prim_data_to_ri_points_polygons, renderman_look_at

# fmt: off

def infinity_cove( ri,width, depth,height, radius, width_divs=20, depth_divs=20, curve_divs=16,height_divs=20):
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
    # The floor should extend from -depth to -radius in the Z direction.
    floor_z = np.linspace(-depth, -radius, depth_divs + 1)
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


def quarter_cylinder_cove(ri,width,radius,width_divs=20,curve_divs=32):
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



def subdiv_cove_volume(ri,width=1.0, height=1.0, depth=1.0, crease=3):
    """
    Create a subdivision surface infinity cove with curved wall-to-floor and wall-to-wall transitions
    Base is at y=0, extending upward to height

    Args:
        width: Width of the cove (X dimension)
        height: Height of the cove (Y dimension)
        depth: Depth of the cove (Z dimension)
        crease: Crease sharpness for all corner transitions (higher = sharper, lower = smoother curve)
    """
    # Half dimensions for X and Z (centered), full height from 0
    hw = width / 2.0
    hd = depth / 2.0

    # 4 faces: bottom (floor), back, left, right
    npolys = [4, 4, 4, 4]

    # Define 8 points - base at y=0, top at y=height
    points = [
        -hw, 0.0, -hd,      # 0: left-bottom-back
        hw,  0.0, -hd,      # 1: right-bottom-back
        -hw, height, -hd,   # 2: left-top-back
        hw,  height, -hd,   # 3: right-top-back
        -hw, 0.0, hd,       # 4: left-bottom-front
        hw,  0.0, hd,       # 5: right-bottom-front
        -hw, height, hd,    # 6: left-top-front
        hw,  height, hd,    # 7: right-top-front
    ]

    # Define 4 faces (bottom, back, left, right)
    indices = [
        0, 1, 5, 4,  # bottom (floor)
        0, 2, 3, 1,  # back wall
        0, 4, 6, 2,  # left wall
        1, 3, 7, 5,  # right wall
    ]

    # Creases: boundary edges (hard) + all corner creases (user-defined for curves)
    nargs = [
        2, 1,  # top of back wall (hard boundary)
        2, 1,  # top of left wall (hard boundary)
        2, 1,  # top of right wall (hard boundary)
        2, 1,  # front edge of floor (hard boundary)
        2, 1,  # front edge of left wall (hard boundary)
        2, 1,  # front edge of right wall (hard boundary)
        2, 1,  # left-back vertical corner (curved transition)
        2, 1,  # right-back vertical corner (curved transition)
        2, 1,  # back-floor horizontal corner (curved transition)
        2, 1,  # left-floor corner (curved transition)
        2, 1,  # right-floor corner (curved transition)
    ]

    intargs = [
        2, 3,   # top of back wall (boundary)
        2, 6,   # top of left wall (boundary)
        3, 7,   # top of right wall (boundary)
        4, 5,   # front edge of floor (boundary)
        4, 6,   # front edge of left wall (boundary)
        5, 7,   # front edge of right wall (boundary)
        0, 2,   # left-back vertical corner
        1, 3,   # right-back vertical corner
        0, 1,   # back-floor horizontal corner
        0, 4,   # left-floor corner
        1, 5,   # right-floor corner
    ]

    # Hard creases (10) for open boundaries only, soft creases for all interior corners
    floatargs = [
        10.0,          # top of back wall
        10.0,          # top of left wall
        10.0,          # top of right wall
        10.0,          # front edge of floor
        10.0,          # front edge of left wall
        10.0,          # front edge of right wall
        float(crease), # left-back vertical corner
        float(crease), # right-back vertical corner
        float(crease), # back-floor horizontal corner
        float(crease), # left-floor corner
        float(crease), # right-floor corner
    ]

    ri.SubdivisionMesh("catmull-clark",npolys, indices, [ri.CREASE] * 11, nargs, intargs, floatargs, {"P": points},)
# fmt: on
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

        ri.TransformBegin()
        ri.Rotate(frame, 0, 1, 0)

        ri.TransformBegin()
        ri.Translate(-4, 0, 0)
        infinity_cove(
            ri, width=4, depth=4, height=10, radius=2, width_divs=20, depth_divs=200, curve_divs=200, height_divs=200
        )

        ri.TransformEnd()

        ri.TransformBegin()
        ri.Translate(0, 0, 0)
        quarter_cylinder_cove(ri, width=4, radius=4, width_divs=200, curve_divs=200)
        ri.TransformEnd()
        ri.TransformBegin()
        ri.Translate(4, 0, 0)
        subdiv_cove_volume(ri, width=4.0, height=4.0, depth=4.0, crease=1.5)
        ri.TransformBegin()
        ri.Rotate(180, 0, 1, 0)
        ri.Scale(2, 2, 2)
        ri.ReadArchive("YourMeshHere.rib.gz")
        ri.TransformEnd()
        ri.TransformEnd()
        ri.TransformEnd()
        ri.WorldEnd()
        ri.FrameEnd()
    ri.End()
