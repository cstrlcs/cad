from build123d import Box, Cylinder, Part, Plane, Pos, extrude

from ender3_cad.dimensions import FACE_FRONT
from ender3_cad.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLES
from ender3_cad.ender3.reference.construction import outline_face
from ender3_cad.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3_cad.ender3.reference.extruder.dimensions import (
    BRACKET_SIDE_PLATE_INNER_Y,
    BRACKET_SIDE_PLATE_LARGE_HOLE_X,
    BRACKET_SIDE_PLATE_LARGE_HOLE_Z,
    BRACKET_SIDE_PLATE_SCREW_HOLES,
    BRACKET_THICKNESS,
    EXTRUDER_MOUNT_LOCATION,
)

BRACKET_SIDE_PLATE_OUTLINE = [
    (-66.5, -79.026431),
    (-75.5, -79.026431),
    (-75.5, -82.1336),
    (-60.613, -92.6892),
    (12.0, -50.4267),
    (12.0, 0.0),
    (-50.0, 0.0),
    (-61.0113, 6.515),
    (-75.5, -5.0378),
    (-75.5, -21.026431),
    (-53.0, -21.026431),
    (-53.0, -66.026431),
    (-66.5, -66.026431),
]
BRACKET_SIDE_PLATE_CORNER_RADII = [
    2.0,
    2.0,
    2.0,
    11.5,
    12.0,
    0.0,
    8.0,
    12.0,
    2.0,
    2.0,
    2.0,
    2.0,
    2.0,
]
BRACKET_SIDE_PLATE_SCREW_HOLE_DIAMETER = 5.1

BRACKET_SIDE_PLATE_LARGE_HOLE_DIAMETER = 7.2

BRACKET_MOTOR_PLATE_OUTLINE = [
    (21.0, -30.5),
    (21.0, 21.0),
    (-24.1771, 21.0),
    (-50.7396, -30.0),
    (-47.8106, -30.0),
    (-47.8106, -32.5),
    (12.0, -32.5),
    (12.0, -30.5),
]
BRACKET_MOTOR_PLATE_CORNER_RADII = [8.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0]
BRACKET_MOTOR_BOSS_HOLE_DIAMETER = 23.0
BRACKET_MOTOR_HOLE_DIAMETER = 3.5
BRACKET_LEAD_SCREW_SLOT_X = -29.8
BRACKET_LEAD_SCREW_SLOT_WIDTH = 10.3
BRACKET_LEAD_SCREW_SLOT_Y_RANGE = (-16.1, -14.6)
BRACKET_LEAD_SCREW_NUT_SLOT_WIDTH = 3.0
BRACKET_LEAD_SCREW_NUT_SLOT_Y_RANGES = [(-25.2, -23.5), (-7.2, -5.5)]


def extruder_motor_bracket() -> Part:
    side_plate = extrude(
        Plane.XZ.offset(-BRACKET_SIDE_PLATE_INNER_Y)
        * outline_face(BRACKET_SIDE_PLATE_OUTLINE, BRACKET_SIDE_PLATE_CORNER_RADII),
        BRACKET_THICKNESS,
    )
    side_plate_y = BRACKET_SIDE_PLATE_INNER_Y - BRACKET_THICKNESS / 2
    side_plate -= [
        Pos(x, side_plate_y, z) * FACE_FRONT * Cylinder(BRACKET_SIDE_PLATE_SCREW_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH)
        for x, z in BRACKET_SIDE_PLATE_SCREW_HOLES
    ]
    side_plate -= (
        Pos(BRACKET_SIDE_PLATE_LARGE_HOLE_X, side_plate_y, BRACKET_SIDE_PLATE_LARGE_HOLE_Z)
        * FACE_FRONT
        * Cylinder(BRACKET_SIDE_PLATE_LARGE_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH)
    )
    motor_plate = extrude(
        Pos(0, 0, -BRACKET_THICKNESS) * outline_face(BRACKET_MOTOR_PLATE_OUTLINE, BRACKET_MOTOR_PLATE_CORNER_RADII),
        BRACKET_THICKNESS,
    )
    motor_plate -= Cylinder(BRACKET_MOTOR_BOSS_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH)
    motor_plate -= [
        Pos(x, y) * Cylinder(BRACKET_MOTOR_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH) for x, y in NEMA17_MOUNTING_HOLES
    ]
    slots = [
        (BRACKET_LEAD_SCREW_SLOT_WIDTH, BRACKET_LEAD_SCREW_SLOT_Y_RANGE),
        *((BRACKET_LEAD_SCREW_NUT_SLOT_WIDTH, y_range) for y_range in BRACKET_LEAD_SCREW_NUT_SLOT_Y_RANGES),
    ]
    for width, (y_start, y_end) in slots:
        motor_plate -= [
            Pos(BRACKET_LEAD_SCREW_SLOT_X, y) * Cylinder(width / 2, CUT_THROUGH_LENGTH) for y in (y_start, y_end)
        ]
        motor_plate -= Pos(BRACKET_LEAD_SCREW_SLOT_X, (y_start + y_end) / 2) * Box(
            width, y_end - y_start, CUT_THROUGH_LENGTH
        )
    bracket = EXTRUDER_MOUNT_LOCATION * (side_plate + motor_plate)
    bracket.label = "extruder_motor_bracket"
    return bracket
