from build123d import Cylinder, Part, Pos

from ender3.dimensions import FACE_FRONT, FACE_RIGHT
from ender3.ender3.reference.profiles.dimensions import CORE_HALF_SIZE
from ender3.ender3.reference.profiles.vslot_2020 import vslot_2020
from ender3.ender3.reference.x_axis.dimensions import (
    LEFT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME,
    RIGHT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME,
    X_BEAM_AXIS_Y,
    X_BEAM_AXIS_Z,
    X_BEAM_LENGTH,
    X_BEAM_SIZE,
    X_BEAM_START,
)

X_BEAM_CORE_SIZE = 2 * CORE_HALF_SIZE
X_BEAM_PLATE_SCREW_TAP_DIAMETER = 3.3
X_BEAM_ACCESS_HOLE_X = [-115.1, 115.1]
X_BEAM_ACCESS_HOLE_DIAMETER = 6.0
X_BEAM_ACCESS_COUNTERBORE_DIAMETER = 11.5
X_BEAM_ACCESS_COUNTERBORE_DEPTH = 4.5


def x_beam() -> Part:
    back_face_y = X_BEAM_AXIS_Y + X_BEAM_SIZE / 2
    beam_screw_holes = LEFT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME + RIGHT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME
    core_holes = [
        Pos(x, X_BEAM_AXIS_Y, X_BEAM_AXIS_Z) * FACE_FRONT * Cylinder(diameter / 2, X_BEAM_CORE_SIZE)
        for diameter, positions in (
            (X_BEAM_PLATE_SCREW_TAP_DIAMETER, [x for x, _ in beam_screw_holes]),
            (X_BEAM_ACCESS_HOLE_DIAMETER, X_BEAM_ACCESS_HOLE_X),
        )
        for x in positions
    ]
    counterbores = [
        Pos(x, back_face_y - X_BEAM_ACCESS_COUNTERBORE_DEPTH / 2, X_BEAM_AXIS_Z)
        * FACE_FRONT
        * Cylinder(X_BEAM_ACCESS_COUNTERBORE_DIAMETER / 2, X_BEAM_ACCESS_COUNTERBORE_DEPTH)
        for x in X_BEAM_ACCESS_HOLE_X
    ]
    beam = X_BEAM_START * FACE_RIGHT * vslot_2020(X_BEAM_LENGTH) - core_holes - counterbores
    beam.label = "x_beam"
    return beam
