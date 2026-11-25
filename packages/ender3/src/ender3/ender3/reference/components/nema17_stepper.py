from typing import NamedTuple

from build123d import Align, Box, Circle, Cylinder, Part, Pos, Rectangle, RectangleRounded, Rot, extrude

from ender3.dimensions import BOTTOM
from ender3.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLES

NEMA17_FLANGE_WIDTH = 42.0
NEMA17_ACROSS_CORNER_CHAMFERS = 53.75
NEMA17_STATOR_WIDTH = 39.0
NEMA17_STATOR_CORNER_RADIUS = 4.0
NEMA17_REAR_CAP_LENGTH = 7.0

NEMA17_MOUNTING_HOLE_DIAMETER = 3.0
NEMA17_FRONT_HOLE_DEPTH = 5.0

NEMA17_FACE_RECESS_DIAMETER = 33.0
NEMA17_FACE_RECESS_DEPTH = 0.5
NEMA17_PILOT_DIAMETER = 22.0
NEMA17_PILOT_HEIGHT = 2.0
NEMA17_PILOT_POCKET_DIAMETER = 7.0
NEMA17_PILOT_POCKET_BOTTOM = -3.0
NEMA17_SHAFT_DIAMETER = 5.0
NEMA17_SHAFT_FLAT_OFFSET = 2.0
NEMA17_CONNECTOR_PROTRUSION = 8.7
NEMA17_CONNECTOR_WIDTH = 17.0


class Nema17Spec(NamedTuple):
    body_length: float
    front_cap_length: float
    rear_hole_depth: float
    connector_height: float
    shaft_length: float
    shaft_has_flat: bool


def nema17_stepper(spec: Nema17Spec) -> Part:
    cap_outline = Rectangle(NEMA17_FLANGE_WIDTH, NEMA17_FLANGE_WIDTH) & Rot(0, 0, 45) * Rectangle(
        NEMA17_ACROSS_CORNER_CHAMFERS, NEMA17_ACROSS_CORNER_CHAMFERS
    )
    stator_length = spec.body_length - spec.front_cap_length - NEMA17_REAR_CAP_LENGTH
    body = (
        Pos(0, 0, -spec.front_cap_length) * extrude(cap_outline, spec.front_cap_length)
        + Pos(0, 0, -spec.body_length + NEMA17_REAR_CAP_LENGTH)
        * extrude(
            RectangleRounded(NEMA17_STATOR_WIDTH, NEMA17_STATOR_WIDTH, NEMA17_STATOR_CORNER_RADIUS), stator_length
        )
        + Pos(0, 0, -spec.body_length) * extrude(cap_outline, NEMA17_REAR_CAP_LENGTH)
    )
    body -= Pos(0, 0, -NEMA17_FACE_RECESS_DEPTH) * Cylinder(
        NEMA17_FACE_RECESS_DIAMETER / 2, NEMA17_FACE_RECESS_DEPTH, align=BOTTOM
    )
    for x, y in NEMA17_MOUNTING_HOLES:
        body -= Pos(x, y, -NEMA17_FRONT_HOLE_DEPTH) * Cylinder(
            NEMA17_MOUNTING_HOLE_DIAMETER / 2, NEMA17_FRONT_HOLE_DEPTH, align=BOTTOM
        )
        body -= Pos(x, y, -spec.body_length) * Cylinder(
            NEMA17_MOUNTING_HOLE_DIAMETER / 2, spec.rear_hole_depth, align=BOTTOM
        )
    body += Pos(0, 0, -NEMA17_FACE_RECESS_DEPTH) * Cylinder(
        NEMA17_PILOT_DIAMETER / 2, NEMA17_FACE_RECESS_DEPTH + NEMA17_PILOT_HEIGHT, align=BOTTOM
    )
    body -= Pos(0, 0, NEMA17_PILOT_POCKET_BOTTOM) * Cylinder(
        NEMA17_PILOT_POCKET_DIAMETER / 2, NEMA17_PILOT_HEIGHT - NEMA17_PILOT_POCKET_BOTTOM, align=BOTTOM
    )
    body += Pos(
        -NEMA17_FLANGE_WIDTH / 2 - NEMA17_CONNECTOR_PROTRUSION / 2, 0, -spec.body_length + spec.connector_height / 2
    ) * Box(NEMA17_CONNECTOR_PROTRUSION, NEMA17_CONNECTOR_WIDTH, spec.connector_height)
    shaft_section = Circle(NEMA17_SHAFT_DIAMETER / 2)
    if spec.shaft_has_flat:
        shaft_section -= Pos(0, NEMA17_SHAFT_FLAT_OFFSET) * Rectangle(
            NEMA17_SHAFT_DIAMETER, NEMA17_SHAFT_DIAMETER, align=(Align.CENTER, Align.MIN)
        )
    return body + Pos(0, 0, NEMA17_PILOT_POCKET_BOTTOM) * extrude(
        shaft_section, spec.shaft_length - NEMA17_PILOT_POCKET_BOTTOM
    )
