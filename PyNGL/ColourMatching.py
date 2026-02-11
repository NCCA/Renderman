from ncca.ngl import Vec3

_checker_linear = [
    ("Dark Skin", (0.180, 0.083, 0.058)),
    ("Light Skin", (0.540, 0.305, 0.223)),
    ("Blue Sky", (0.122, 0.198, 0.337)),
    ("Foliage", (0.095, 0.150, 0.057)),
    ("Blue Flower", (0.240, 0.215, 0.445)),
    ("Bluish Green", (0.134, 0.503, 0.401)),
    ("Orange", (0.672, 0.214, 0.032)),
    ("Purplish Blue", (0.081, 0.104, 0.380)),
    ("Moderate Red", (0.527, 0.104, 0.129)),
    ("Purple", (0.109, 0.041, 0.149)),
    ("Yellow Green", (0.338, 0.510, 0.055)),
    ("Orange Yellow", (0.752, 0.367, 0.035)),
    ("Blue", (0.040, 0.046, 0.305)),
    ("Green", (0.063, 0.296, 0.067)),
    ("Red", (0.428, 0.035, 0.045)),
    ("Yellow", (0.812, 0.594, 0.013)),
    ("Magenta", (0.496, 0.095, 0.306)),
    ("Cyan", (0.003, 0.245, 0.356)),
    ("White", (0.897, 0.897, 0.893)),
    ("Neutral 8", (0.604, 0.604, 0.604)),
    ("Neutral 6.5", (0.352, 0.352, 0.352)),
    ("Neutral 5", (0.203, 0.203, 0.201)),
    ("Neutral 3.5", (0.089, 0.089, 0.089)),
    ("Black", (0.034, 0.034, 0.034)),
]


def render_colorchecker(ri, patch_size=1.0, gap=0.1):
    """
    Render a 6x4 color checker grid with a backing plane
    """

    cols = 6
    rows = 4

    total_width = cols * patch_size + (cols - 1) * gap
    total_height = rows * patch_size + (rows - 1) * gap

    # --------------------------------------------------
    # Backing plane (slightly larger, slightly behind)
    # --------------------------------------------------

    padding = patch_size * 0.2
    z_offset = -0.01  # small offset behind patches

    half_w = (total_width * 0.5) + padding
    half_h = (total_height * 0.5) + padding
    P_bg = [-half_w, half_h, z_offset, half_w, half_h, z_offset, half_w, -half_h, z_offset, -half_w, -half_h, z_offset]

    ri.AttributeBegin()
    ri.Bxdf("PxrBlack", "checker_backing")
    ri.Polygon({"P": P_bg})
    ri.AttributeEnd()
    # --------------------------------------------------
    # Render color patches
    # --------------------------------------------------

    start_x = -total_width * 0.5
    start_y = total_height * 0.5

    for i, (_, colour) in enumerate(_checker_linear):
        row = i // cols
        col = (cols - 1) - (i % cols)
        x = start_x + col * (patch_size + gap)
        y = start_y - row * (patch_size + gap)

        P = [x, y, 0, x + patch_size, y, 0, x + patch_size, y - patch_size, 0, x, y - patch_size, 0]
        ri.AttributeBegin()
        # ri.Bxdf("PxrDiffuse", f"diffuse_{i}", {"color diffuseColor": colour})
        ri.Bxdf("PxrConstant", f"constant_{i}", {"color emitColor": colour})
        ri.Polygon({"P": P})
        ri.AttributeEnd()


def render_refballs(ri, position, scale):
    # Spheres
    ri.AttributeBegin()
    ri.TransformBegin()
    ri.Translate(position[0], position[1], position[2])
    ri.TransformBegin()
    ri.Translate(-scale[0] - 0.1, 0, 0)
    ri.Scale(scale[0], scale[1], scale[2])
    ri.Bxdf("PxrDiffuse", "grey", {"color diffuseColor": [0.19, 0.19, 0.19]})
    ri.Sphere(1, -1, 1, 360)
    ri.TransformEnd()
    ri.TransformBegin()
    ri.Translate(scale[0] + 0.1, 0, 0)
    ri.Scale(scale[0], scale[1], scale[2])
    ri.Bxdf("LamaConductor", "conductor", {"color tint": [0.5, 0.5, 0.5]})

    ri.Sphere(1, -1, 1, 360)
    ri.TransformEnd()
    ri.TransformEnd()
    ri.AttributeEnd()
