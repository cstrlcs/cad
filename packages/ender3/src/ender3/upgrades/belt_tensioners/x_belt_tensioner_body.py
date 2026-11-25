from build123d import Part

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M4_CLEARANCE_DIAMETER
from ender3.ender3.reference.profiles.dimensions import CELL_HALF_SIZE
from ender3.ender3.reference.x_axis.dimensions import (
    X_BEAM_AXIS_Y,
    X_BEAM_AXIS_Z,
    X_BEAM_LENGTH,
    X_BEAM_X_MIN,
    X_TENSIONER_END_CENTERS_X,
    X_TENSIONER_SCREW_HOLES_IN_TENSIONER_FRAME,
    X_TENSIONER_WIDTH,
)
from ender3.upgrades.belt_tensioners.construction import case_channel, hole_along_w, stem_hole
from ender3.upgrades.belt_tensioners.dimensions import (
    CASE_W_RANGE,
    PRINT_FROM_END_WALL,
    X_IDLER_CENTER,
    X_IDLER_TRAVEL,
    X_TENSIONER_LOCATION,
)

X_BEAM_END_U = X_BEAM_X_MIN + X_BEAM_LENGTH - X_IDLER_CENTER.X
X_BEAM_FRONT_W = X_BEAM_AXIS_Y - CELL_HALF_SIZE - X_IDLER_CENTER.Y
X_BEAM_V_RANGE = (X_BEAM_AXIS_Z - CELL_HALF_SIZE - X_IDLER_CENTER.Z, X_BEAM_AXIS_Z + CELL_HALF_SIZE - X_IDLER_CENTER.Z)
X_TONGUE_START_U = X_TENSIONER_END_CENTERS_X[0] - X_TENSIONER_WIDTH / 2 - X_IDLER_CENTER.X
X_TONGUE_SCREW_HOLES = [
    (x - X_IDLER_CENTER.X, X_BEAM_AXIS_Z + z - X_IDLER_CENTER.Z) for x, z in X_TENSIONER_SCREW_HOLES_IN_TENSIONER_FRAME
]


def x_belt_tensioner_body() -> Part:
    tongue_w = (CASE_W_RANGE[0], X_BEAM_FRONT_W)
    body = case_channel(X_BEAM_END_U, X_IDLER_TRAVEL)
    body += block((X_TONGUE_START_U, X_BEAM_END_U), tongue_w, X_BEAM_V_RANGE)
    body -= [hole_along_w(u, v, M4_CLEARANCE_DIAMETER, tongue_w) for u, v in X_TONGUE_SCREW_HOLES]
    body -= stem_hole(X_IDLER_TRAVEL)
    body = X_TENSIONER_LOCATION * body
    body.label = "x_belt_tensioner_body"
    body.color = PRINTED_PART_COLOR
    return body


def x_belt_tensioner_body_for_printing() -> Part:
    return resting_on_bed(PRINT_FROM_END_WALL * X_TENSIONER_LOCATION.inverse() * x_belt_tensioner_body())
