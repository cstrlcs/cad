from build123d import Part, Plane, extrude

from ender3.construction import block
from ender3.ender3.reference.construction import circles, outline_face

Z_ENDSTOP_BRACKET_LEFT_FACE_X = -170.0
Z_ENDSTOP_BRACKET_THICKNESS = 5.0
Z_ENDSTOP_BRACKET_OUTLINE_YZ = [(0.0, 81.5), (0.0, 32.0), (-20.0, 32.0), (-20.0, 61.0), (-41.0, 61.0), (-41.0, 81.5)]
Z_ENDSTOP_BRACKET_OUTLINE_RADII = [3.0, 1.0, 1.0, 3.0, 3.0, 3.0]
Z_ENDSTOP_BRACKET_KEY_Y_RANGE = (-24.0, -20.0)
Z_ENDSTOP_BRACKET_KEY_Z_RANGE = (40.0, 45.0)
Z_ENDSTOP_BRACKET_KEY_PROTRUSION = 2.0
Z_ENDSTOP_BRACKET_FRAME_SCREW_HOLES_YZ = [(-10.0, 60.0), (-10.0, 75.5)]
Z_ENDSTOP_BRACKET_FRAME_SCREW_HOLE_DIAMETER = 4.5
Z_ENDSTOP_SWITCH_SCREW_HOLES_YZ = [(-38.5, 64.95), (-23.5, 64.95)]
Z_ENDSTOP_SWITCH_SCREW_HOLE_DIAMETER = 2.9
Z_ENDSTOP_SWITCH_POCKET_YZ = [
    (-22.45, 72.78),
    (-26.95, 72.78),
    (-26.95, 64.95),
    (-35.05, 64.95),
    (-35.05, 72.78),
    (-38.05, 72.78),
    (-38.05, 78.9531),
    (-22.45, 78.9531),
]
Z_ENDSTOP_SWITCH_POCKET_CORNER_RADIUS = 0.8
Z_ENDSTOP_SWITCH_POCKET_DEPTH = 2.5


def z_endstop_bracket() -> Part:
    plate_plane = Plane.YZ.offset(Z_ENDSTOP_BRACKET_LEFT_FACE_X)
    pocket_plane = Plane.YZ.offset(Z_ENDSTOP_BRACKET_LEFT_FACE_X + Z_ENDSTOP_BRACKET_THICKNESS)
    outline = (
        outline_face(Z_ENDSTOP_BRACKET_OUTLINE_YZ, Z_ENDSTOP_BRACKET_OUTLINE_RADII)
        - circles(Z_ENDSTOP_BRACKET_FRAME_SCREW_HOLES_YZ, Z_ENDSTOP_BRACKET_FRAME_SCREW_HOLE_DIAMETER)
        - circles(Z_ENDSTOP_SWITCH_SCREW_HOLES_YZ, Z_ENDSTOP_SWITCH_SCREW_HOLE_DIAMETER)
    )
    pocket = outline_face(Z_ENDSTOP_SWITCH_POCKET_YZ, Z_ENDSTOP_SWITCH_POCKET_CORNER_RADIUS)
    key = block(
        (
            Z_ENDSTOP_BRACKET_LEFT_FACE_X,
            Z_ENDSTOP_BRACKET_LEFT_FACE_X + Z_ENDSTOP_BRACKET_THICKNESS + Z_ENDSTOP_BRACKET_KEY_PROTRUSION,
        ),
        Z_ENDSTOP_BRACKET_KEY_Y_RANGE,
        Z_ENDSTOP_BRACKET_KEY_Z_RANGE,
    )
    bracket = (
        extrude(plate_plane * outline, Z_ENDSTOP_BRACKET_THICKNESS)
        + key
        - extrude(pocket_plane * pocket, -Z_ENDSTOP_SWITCH_POCKET_DEPTH)
    )
    bracket.label = "z_endstop_bracket"
    return bracket
