from build123d import Box, Part, Pos

from ender3_cad.dimensions import FACE_DOWN, FACE_RIGHT
from ender3_cad.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3_cad.ender3.reference.frame.construction import bore_into_face, through_hole
from ender3_cad.ender3.reference.frame.dimensions import (
    CLEARANCE_HOLE_DIAMETER,
    CROSS_MEMBER_ENCLOSURE_NOTCH_HEIGHT,
    CROSS_MEMBER_ENCLOSURE_NOTCH_X_RANGE,
    CROSS_MEMBER_LOCATION,
    PROFILE_4040_HALF_SIZE,
    WIDE_COUNTERBORE_DEPTH,
    WIDE_COUNTERBORE_DIAMETER,
)
from ender3_cad.ender3.reference.profiles.vslot_4040 import vslot_4040

CROSS_MEMBER_LENGTH = 250.0
CROSS_MEMBER_Y_RAIL_NOTCH_WIDTH = 40.0
CROSS_MEMBER_Y_RAIL_NOTCH_DEPTH = 7.0

CROSS_MEMBER_Y_RAIL_JOINT_HOLES = [(-10.0, -10.0), (-10.0, 10.0), (10.0, -10.0), (10.0, 10.0)]
CROSS_MEMBER_ENCLOSURE_HOLE_DIAMETER = 2.5
CROSS_MEMBER_ENCLOSURE_HOLES = [(-67.0, -10.0)]


def middle_cross_member() -> Part:
    member = Pos(-CROSS_MEMBER_LENGTH / 2, 0, 0) * FACE_RIGHT * vslot_4040(CROSS_MEMBER_LENGTH)
    y_rail_notch = Pos(0, 0, PROFILE_4040_HALF_SIZE) * Box(
        CROSS_MEMBER_Y_RAIL_NOTCH_WIDTH, CUT_THROUGH_LENGTH, 2 * CROSS_MEMBER_Y_RAIL_NOTCH_DEPTH
    )
    notch_start, notch_end = CROSS_MEMBER_ENCLOSURE_NOTCH_X_RANGE
    enclosure_notch = Pos((notch_start + notch_end) / 2, 0, -PROFILE_4040_HALF_SIZE) * Box(
        notch_end - notch_start, CUT_THROUGH_LENGTH, 2 * CROSS_MEMBER_ENCLOSURE_NOTCH_HEIGHT
    )
    y_rail_joints = [
        tool
        for x, y in CROSS_MEMBER_Y_RAIL_JOINT_HOLES
        for tool in (
            Pos(x, y, 0) * through_hole(CLEARANCE_HOLE_DIAMETER),
            Pos(x, y, -PROFILE_4040_HALF_SIZE)
            * FACE_DOWN
            * bore_into_face(WIDE_COUNTERBORE_DIAMETER, WIDE_COUNTERBORE_DEPTH),
        )
    ]
    enclosure_holes = [
        Pos(x, y, 0) * through_hole(CROSS_MEMBER_ENCLOSURE_HOLE_DIAMETER) for x, y in CROSS_MEMBER_ENCLOSURE_HOLES
    ]
    member = CROSS_MEMBER_LOCATION * (member - y_rail_notch - enclosure_notch - y_rail_joints - enclosure_holes)
    member.label = "middle_cross_member"
    return member
