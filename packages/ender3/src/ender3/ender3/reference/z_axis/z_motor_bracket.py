from build123d import Box, Cone, Cylinder, Part, Pos, fillet

from ender3.dimensions import BOTTOM, FACE_BACK, FACE_FRONT
from ender3.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLE_SPACING
from ender3.ender3.reference.z_axis.dimensions import LEAD_SCREW_AXIS_X

Z_MOTOR_BRACKET_CENTER = Pos(LEAD_SCREW_AXIS_X, 5.0, 79.75)
Z_MOTOR_BRACKET_SIZE = (42.0, 10.0, 12.0)
Z_MOTOR_BRACKET_EDGE_RADIUS = 1.5
Z_MOTOR_BRACKET_FRAME_SCREW_X_FROM_CENTER = [-10.0, 10.0]
Z_MOTOR_BRACKET_FRAME_SCREW_HOLE_DIAMETER = 5.0
Z_MOTOR_BRACKET_FRAME_SCREW_COUNTERSINK_DIAMETER = 11.0
Z_MOTOR_BRACKET_MOTOR_SCREW_OFFSET_Y = 0.5
Z_MOTOR_BRACKET_MOTOR_SCREW_HOLES_FROM_CENTER = [
    (x, Z_MOTOR_BRACKET_MOTOR_SCREW_OFFSET_Y)
    for x in (-NEMA17_MOUNTING_HOLE_SPACING / 2, NEMA17_MOUNTING_HOLE_SPACING / 2)
]
Z_MOTOR_BRACKET_MOTOR_SCREW_HOLE_DIAMETER = 3.5
Z_MOTOR_BRACKET_COUPLER_CLEARANCE_OFFSET_Y = 11.5472
Z_MOTOR_BRACKET_COUPLER_CLEARANCE_DIAMETER = 19.0


def z_motor_bracket() -> Part:
    length, depth, height = Z_MOTOR_BRACKET_SIZE
    block = Box(length, depth, height)
    countersink_depth = (
        Z_MOTOR_BRACKET_FRAME_SCREW_COUNTERSINK_DIAMETER - Z_MOTOR_BRACKET_FRAME_SCREW_HOLE_DIAMETER
    ) / 2
    frame_screws = [
        Pos(x, 0, 0) * FACE_FRONT * Cylinder(Z_MOTOR_BRACKET_FRAME_SCREW_HOLE_DIAMETER / 2, depth)
        for x in Z_MOTOR_BRACKET_FRAME_SCREW_X_FROM_CENTER
    ]
    countersinks = [
        Pos(x, depth / 2 - countersink_depth, 0)
        * FACE_BACK
        * Cone(
            Z_MOTOR_BRACKET_FRAME_SCREW_HOLE_DIAMETER / 2,
            Z_MOTOR_BRACKET_FRAME_SCREW_COUNTERSINK_DIAMETER / 2,
            countersink_depth,
            align=BOTTOM,
        )
        for x in Z_MOTOR_BRACKET_FRAME_SCREW_X_FROM_CENTER
    ]
    motor_screws = [
        Pos(x, y, 0) * Cylinder(Z_MOTOR_BRACKET_MOTOR_SCREW_HOLE_DIAMETER / 2, height)
        for x, y in Z_MOTOR_BRACKET_MOTOR_SCREW_HOLES_FROM_CENTER
    ]
    coupler_clearance = Pos(0, Z_MOTOR_BRACKET_COUPLER_CLEARANCE_OFFSET_Y, 0) * Cylinder(
        Z_MOTOR_BRACKET_COUPLER_CLEARANCE_DIAMETER / 2, height
    )
    bracket = Z_MOTOR_BRACKET_CENTER * (
        fillet(block.edges(), Z_MOTOR_BRACKET_EDGE_RADIUS)
        - frame_screws
        - countersinks
        - motor_screws
        - coupler_clearance
    )
    bracket.label = "z_motor_bracket"
    return bracket
