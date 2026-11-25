from build123d import Box, Part, Pos

from ender3.dimensions import BOTTOM


def centered_block(center: tuple[float, float], size: tuple[float, float, float], bottom_z: float) -> Part:
    (x, y), (dx, dy, dz) = center, size
    return Pos(x, y, bottom_z) * Box(dx, dy, dz, align=BOTTOM)
