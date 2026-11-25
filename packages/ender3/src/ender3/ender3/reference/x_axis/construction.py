from build123d import Face, Line, RadiusArc, Wire


def arc_outline_face(points: list[tuple[float, float]], segment_radii: list[float]) -> Face:
    ends = points[1:] + points[:1]
    return Face(
        Wire(
            [
                RadiusArc(start, end, radius) if radius else Line(start, end)
                for start, end, radius in zip(points, ends, segment_radii, strict=True)
            ]
        )
    )
