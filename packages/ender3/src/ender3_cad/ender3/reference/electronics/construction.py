from build123d import Cylinder, Part

THIN_PLATE_HOLE_LENGTH = 10.0


def thin_plate_hole(diameter: float) -> Part:
    return Cylinder(diameter / 2, THIN_PLATE_HOLE_LENGTH)
