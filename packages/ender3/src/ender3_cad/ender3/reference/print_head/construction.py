from build123d import Pos


def on_hole_axis(hole_point: tuple[float, float, float], y: float) -> Pos:
    x, _, z = hole_point
    return Pos(x, y, z)
