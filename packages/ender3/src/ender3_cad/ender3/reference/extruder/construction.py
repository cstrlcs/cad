from build123d import Cylinder, Part, Pos

from ender3_cad.dimensions import FACE_RIGHT


def x_cylinder(diameter: float, x_start: float, x_end: float, y: float, z: float) -> Part:
    return Pos((x_start + x_end) / 2, y, z) * FACE_RIGHT * Cylinder(diameter / 2, x_end - x_start)
