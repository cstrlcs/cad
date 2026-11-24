from build123d import Part, Pos

from ender3_cad.dimensions import FACE_RIGHT
from ender3_cad.ender3.reference.frame.construction import bore_into_face, through_hole
from ender3_cad.ender3.reference.frame.dimensions import (
    CLEARANCE_HOLE_DIAMETER,
    WIDE_COUNTERBORE_DEPTH,
    WIDE_COUNTERBORE_DIAMETER,
)
from ender3_cad.ender3.reference.profiles.dimensions import CELL_HALF_SIZE
from ender3_cad.ender3.reference.profiles.vslot_2020 import vslot_2020

TOP_BAR_LENGTH = 330.0
TOP_BAR_UPRIGHT_JOINT_HOLES = [(-155.0, 0.0), (-135.0, 0.0), (135.0, 0.0), (155.0, 0.0)]
TOP_BAR_LOCATION = Pos(0, -10, 450)


def top_bar() -> Part:
    bar = Pos(-TOP_BAR_LENGTH / 2, 0, 0) * FACE_RIGHT * vslot_2020(TOP_BAR_LENGTH)
    upright_joints = [
        tool
        for x, y in TOP_BAR_UPRIGHT_JOINT_HOLES
        for tool in (
            Pos(x, y, 0) * through_hole(CLEARANCE_HOLE_DIAMETER),
            Pos(x, y, CELL_HALF_SIZE) * bore_into_face(WIDE_COUNTERBORE_DIAMETER, WIDE_COUNTERBORE_DEPTH),
        )
    ]
    bar = TOP_BAR_LOCATION * (bar - upright_joints)
    bar.label = "top_bar"
    return bar
