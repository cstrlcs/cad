from math import radians, tan

from build123d import Cone, Cylinder, Part, Pos

from ender3.dimensions import FACE_BACK, FACE_DOWN, FACE_FRONT, FACE_LEFT, FACE_RIGHT, TOP
from ender3.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3.ender3.reference.frame.dimensions import (
    BASE_RAIL_LENGTH,
    CLEARANCE_HOLE_DIAMETER,
    PROFILE_4040_HALF_SIZE,
    TAP_DRILL_DIAMETER,
    WIDE_COUNTERBORE_DEPTH,
    WIDE_COUNTERBORE_DIAMETER,
)
from ender3.ender3.reference.profiles.vslot_4040 import vslot_4040

NARROW_COUNTERBORE_DIAMETER = 9.5
NARROW_COUNTERBORE_DEPTH = 5.8

TAPPED_HOLE_DEPTH = 18.0
TAPPED_HOLE_CHAMFER_DIAMETER = 5.0
DRILL_POINT_HALF_ANGLE = 59.0
END_CAP_PEG_COUNTERBORE_DIAMETER = 6.0
END_CAP_PEG_COUNTERBORE_DEPTH = 12.0

BASE_RAIL_CROSS_MEMBER_JOINT_HOLES = [(135.0, -10.0), (155.0, 10.0)]
BASE_RAIL_UPRIGHT_JOINT_HOLES = [(-10.0, 145.0), (10.0, 145.0)]
BASE_RAIL_FRONT_TAPPED_HOLES = [(-10.0, -10.0), (-10.0, 10.0), (10.0, -10.0), (10.0, 10.0)]
BASE_RAIL_BACK_TAPPED_HOLES = [(-10.0, 10.0), (10.0, -10.0)]
BASE_RAIL_BACK_END_CAP_PEG_HOLES = [(-10.0, -10.0), (10.0, 10.0)]


def bore_into_face(diameter: float, depth: float) -> Part:
    return Cylinder(diameter / 2, depth, align=TOP)


def through_hole(diameter: float) -> Part:
    return Cylinder(diameter / 2, CUT_THROUGH_LENGTH)


def chamfer_cone(hole_diameter: float, chamfer_diameter: float) -> Part:
    hole_radius, chamfer_radius = hole_diameter / 2, chamfer_diameter / 2
    return Cone(hole_radius, chamfer_radius, chamfer_radius - hole_radius, align=TOP)


def _tapped_end_hole() -> Part:
    drill_radius = TAP_DRILL_DIAMETER / 2
    drill_point_height = drill_radius / tan(radians(DRILL_POINT_HALF_ANGLE))
    return (
        chamfer_cone(TAP_DRILL_DIAMETER, TAPPED_HOLE_CHAMFER_DIAMETER)
        + Cylinder(drill_radius, TAPPED_HOLE_DEPTH, align=TOP)
        + Pos(0, 0, -TAPPED_HOLE_DEPTH) * Cone(0, drill_radius, drill_point_height, align=TOP)
    )


def base_rail() -> Part:
    rail = FACE_BACK * vslot_4040(BASE_RAIL_LENGTH)
    cross_member_joints = [
        tool
        for y, z in BASE_RAIL_CROSS_MEMBER_JOINT_HOLES
        for tool in (
            Pos(0, y, z) * FACE_RIGHT * through_hole(CLEARANCE_HOLE_DIAMETER),
            Pos(-PROFILE_4040_HALF_SIZE, y, z)
            * FACE_LEFT
            * bore_into_face(WIDE_COUNTERBORE_DIAMETER, WIDE_COUNTERBORE_DEPTH),
            Pos(PROFILE_4040_HALF_SIZE, y, z)
            * FACE_RIGHT
            * bore_into_face(NARROW_COUNTERBORE_DIAMETER, NARROW_COUNTERBORE_DEPTH),
        )
    ]
    upright_joints = [
        tool
        for x, y in BASE_RAIL_UPRIGHT_JOINT_HOLES
        for tool in (
            Pos(x, y, 0) * through_hole(CLEARANCE_HOLE_DIAMETER),
            Pos(x, y, PROFILE_4040_HALF_SIZE) * bore_into_face(WIDE_COUNTERBORE_DIAMETER, WIDE_COUNTERBORE_DEPTH),
            Pos(x, y, -PROFILE_4040_HALF_SIZE)
            * FACE_DOWN
            * bore_into_face(NARROW_COUNTERBORE_DIAMETER, NARROW_COUNTERBORE_DEPTH),
        )
    ]
    front_end = [Pos(x, 0, z) * FACE_FRONT * _tapped_end_hole() for x, z in BASE_RAIL_FRONT_TAPPED_HOLES]
    back_end = [
        Pos(x, BASE_RAIL_LENGTH, z) * FACE_BACK * _tapped_end_hole() for x, z in BASE_RAIL_BACK_TAPPED_HOLES
    ] + [
        Pos(x, BASE_RAIL_LENGTH, z)
        * FACE_BACK
        * (_tapped_end_hole() + bore_into_face(END_CAP_PEG_COUNTERBORE_DIAMETER, END_CAP_PEG_COUNTERBORE_DEPTH))
        for x, z in BASE_RAIL_BACK_END_CAP_PEG_HOLES
    ]
    return rail - cross_member_joints - upright_joints - front_end - back_end
