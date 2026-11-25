from collections.abc import Iterable

from build123d import Align, Circle, Face, FilletPolyline, Location, Part, Pos, Rectangle, make_face


def placed(part: Part, location: Location, label: str) -> Part:
    result = location * part
    result.label = label
    return result


def printer_point(location: Location, x: float, y: float, z: float) -> tuple[float, float, float]:
    return tuple((location * Pos(x, y, z)).position)


def circles(points: Iterable[tuple[float, float]], diameter: float) -> list[Circle]:
    return [Pos(*point) * Circle(diameter / 2) for point in points]


def range_rectangle(x_range: tuple[float, float], y_range: tuple[float, float]) -> Rectangle:
    (x0, x1), (y0, y1) = x_range, y_range
    return Pos(x0, y0) * Rectangle(x1 - x0, y1 - y0, align=Align.MIN)


def outline_face(points: Iterable[tuple[float, float]], corner_radii: float | Iterable[float]) -> Face:
    return make_face(FilletPolyline(*points, radius=corner_radii, close=True))
