from build123d import Part, Pos

from ender3.dimensions import FACE_BACK, FACE_DOWN, FACE_FRONT
from ender3.ender3.reference.frame.construction import bore_into_face, chamfer_cone
from ender3.ender3.reference.frame.dimensions import (
    BORE_CHAMFER_DIAMETER,
    PROFILE_4040_HALF_SIZE,
    TAP_DRILL_DIAMETER,
    Y_RAIL_LENGTH,
    Y_RAIL_LOCATION,
)
from ender3.ender3.reference.profiles.dimensions import CENTER_BORE_DIAMETER
from ender3.ender3.reference.profiles.vslot_4040 import vslot_4040

Y_RAIL_BORES = [(-10.0, -10.0), (-10.0, 10.0), (10.0, -10.0), (10.0, 10.0)]
Y_RAIL_CROSS_MEMBER_JOINT_HOLES = [(-10.0, 205.0), (-10.0, 225.0), (10.0, 205.0), (10.0, 225.0)]
Y_RAIL_JOINT_HOLE_DEPTH = 14.0


def y_rail() -> Part:
    rail = FACE_BACK * vslot_4040(Y_RAIL_LENGTH)
    bore_chamfers = [
        Pos(x, 0, z) * FACE_FRONT * chamfer_cone(CENTER_BORE_DIAMETER, BORE_CHAMFER_DIAMETER) for x, z in Y_RAIL_BORES
    ] + [
        Pos(x, Y_RAIL_LENGTH, z) * FACE_BACK * chamfer_cone(CENTER_BORE_DIAMETER, BORE_CHAMFER_DIAMETER)
        for x, z in Y_RAIL_BORES
    ]
    cross_member_joints = [
        Pos(x, y, -PROFILE_4040_HALF_SIZE) * FACE_DOWN * bore_into_face(TAP_DRILL_DIAMETER, Y_RAIL_JOINT_HOLE_DEPTH)
        for x, y in Y_RAIL_CROSS_MEMBER_JOINT_HOLES
    ]
    rail = Y_RAIL_LOCATION * (rail - bore_chamfers - cross_member_joints)
    rail.label = "y_rail"
    return rail
