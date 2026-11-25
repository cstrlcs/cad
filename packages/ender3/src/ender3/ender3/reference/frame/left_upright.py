from build123d import Part, Pos

from ender3.dimensions import FACE_BACK, FACE_DOWN
from ender3.ender3.reference.frame.construction import chamfer_cone, through_hole
from ender3.ender3.reference.frame.dimensions import BORE_CHAMFER_DIAMETER, UPRIGHT_LENGTH, WIDE_FACE_ALONG_X
from ender3.ender3.reference.profiles.dimensions import CENTER_BORE_DIAMETER
from ender3.ender3.reference.profiles.vslot_2040 import vslot_2040

UPRIGHT_BORES = [(-10.0, 0.0), (10.0, 0.0)]

LEFT_UPRIGHT_Z_MOTOR_BRACKET_HOLE_DIAMETER = 2.5
LEFT_UPRIGHT_Z_MOTOR_BRACKET_HOLES = [(-10.0, 39.75), (10.0, 39.75)]

LEFT_UPRIGHT_LOCATION = Pos(-145, -10, 40)


def left_upright() -> Part:
    upright = WIDE_FACE_ALONG_X * vslot_2040(UPRIGHT_LENGTH)
    z_motor_bracket_holes = [
        Pos(x, 0, z) * FACE_BACK * through_hole(LEFT_UPRIGHT_Z_MOTOR_BRACKET_HOLE_DIAMETER)
        for x, z in LEFT_UPRIGHT_Z_MOTOR_BRACKET_HOLES
    ]
    bore_chamfers = [
        Pos(x, y, 0) * FACE_DOWN * chamfer_cone(CENTER_BORE_DIAMETER, BORE_CHAMFER_DIAMETER) for x, y in UPRIGHT_BORES
    ] + [
        Pos(x, y, UPRIGHT_LENGTH) * chamfer_cone(CENTER_BORE_DIAMETER, BORE_CHAMFER_DIAMETER) for x, y in UPRIGHT_BORES
    ]
    upright = LEFT_UPRIGHT_LOCATION * (upright - z_motor_bracket_holes - bore_chamfers)
    upright.label = "left_upright"
    return upright
