from build123d import Axis, Part, Plane, Polygon, revolve

V_WHEEL_BORE_RADIUS = 8.0
V_WHEEL_BEARING_STOP_RADIUS = 6.8
V_WHEEL_BEARING_STOP_HALF_WIDTH = 0.5
V_WHEEL_HALF_WIDTH = 5.1
V_WHEEL_SIDE_FACE_RADIUS = 10.0
V_WHEEL_OUTER_RADIUS = 12.05
V_WHEEL_CREST_HALF_WIDTH = 3.05
V_WHEEL_EDGE_CHAMFER = 0.1


def v_wheel() -> Part:
    bore, stop, chamfer = V_WHEEL_BORE_RADIUS, V_WHEEL_BEARING_STOP_RADIUS, V_WHEEL_EDGE_CHAMFER
    half, stop_half = V_WHEEL_HALF_WIDTH, V_WHEEL_BEARING_STOP_HALF_WIDTH
    half_profile = [
        (bore + chamfer, half),
        (V_WHEEL_SIDE_FACE_RADIUS, half),
        (V_WHEEL_OUTER_RADIUS, V_WHEEL_CREST_HALF_WIDTH),
    ]
    stop_profile = [(bore, stop_half), (stop + chamfer, stop_half), (stop, stop_half - chamfer)]
    upper = [*half_profile, *[(r, -z) for r, z in reversed(half_profile)], (bore, -half + chamfer)]
    lower = [*[(r, -z) for r, z in stop_profile], *reversed(stop_profile), (bore, half - chamfer)]
    wheel = revolve(Plane.XZ * Polygon(*upper, *lower, align=None), Axis.Z)
    wheel.label = "v_wheel"
    return wheel
