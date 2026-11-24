from build123d import Part, Pos

from ender3_cad.dimensions import FACE_BACK
from ender3_cad.ender3.reference.frame.construction import through_hole
from ender3_cad.ender3.reference.frame.dimensions import UPRIGHT_LENGTH, WIDE_FACE_ALONG_X
from ender3_cad.ender3.reference.profiles.vslot_2040 import vslot_2040

RIGHT_UPRIGHT_PSU_HOLE_DIAMETER = 4.5
RIGHT_UPRIGHT_PSU_HOLES = [(-10.0, 80.0), (-10.0, 230.0)]

RIGHT_UPRIGHT_LOCATION = Pos(145, -10, 40)


def right_upright() -> Part:
    upright = WIDE_FACE_ALONG_X * vslot_2040(UPRIGHT_LENGTH)
    psu_holes = [
        Pos(x, 0, z) * FACE_BACK * through_hole(RIGHT_UPRIGHT_PSU_HOLE_DIAMETER) for x, z in RIGHT_UPRIGHT_PSU_HOLES
    ]
    upright = RIGHT_UPRIGHT_LOCATION * (upright - psu_holes)
    upright.label = "right_upright"
    return upright
