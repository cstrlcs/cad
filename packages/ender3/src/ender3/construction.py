from build123d import Align, Box, Part, Pos, Rot


def block(x_range: tuple[float, float], y_range: tuple[float, float], z_range: tuple[float, float]) -> Part:
    (x0, x1), (y0, y1), (z0, z1) = x_range, y_range, z_range
    return Pos(x0, y0, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=Align.MIN)


def resting_on_bed(part: Part) -> Part:
    return Pos(0, 0, -part.bounding_box().min.Z) * part


def ceiling_on_bed(part: Part) -> Part:
    return resting_on_bed(Rot(0, 180, 0) * part)
