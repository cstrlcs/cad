from build123d import Cone, Part, Plane, mirror

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.reference.y_axis.dimensions import (
    Y_BELT_TENSIONER_SLOT_CENTERS,
    Y_BELT_TENSIONER_SLOT_WIDTH,
    Y_PROFILE_FRONT_END,
)
from ender3_cad.upgrades.belt_tensioners.construction import case_channel, end_wall_u_range, hole_along_w, stem_hole
from ender3_cad.upgrades.belt_tensioners.dimensions import (
    CASE_HALF_HEIGHT,
    CASE_INNER_HALF_HEIGHT,
    PRINT_FROM_END_WALL,
    Y_IDLER_CENTER,
    Y_IDLER_TRAVEL,
    Y_RAIL_HALF_SIZE,
    Y_TENSIONER_HALF_WIDTH,
    Y_TENSIONER_LOCATION,
)

M5_HEAD_DIAMETER = 8.5
BOLT_ACCESS_MARGIN = 1.0

M4_COUNTERSINK_DIAMETER = 8.4
M4_COUNTERSINK_DEPTH = 2.2

Y_RAIL_END_U = Y_IDLER_CENTER.Y - Y_PROFILE_FRONT_END[1]
Y_RAIL_BOTTOM_V = Y_PROFILE_FRONT_END[2] - Y_RAIL_HALF_SIZE - Y_IDLER_CENTER.Z
Y_RAIL_SLOT_V = Y_PROFILE_FRONT_END[2] + Y_BELT_TENSIONER_SLOT_CENTERS[0][1] - Y_IDLER_CENTER.Z

Y_EAR_LENGTH_ALONG_RAIL = 18.0
Y_EAR_SCREW_INSET_FROM_RAIL_END = 10.0
Y_EAR_SCREW_U = Y_RAIL_END_U - Y_EAR_SCREW_INSET_FROM_RAIL_END
Y_EAR_SCREW_DIAMETER = Y_BELT_TENSIONER_SLOT_WIDTH
Y_WHEEL_CLEARANCE_TOP_V = -CASE_HALF_HEIGHT


def _y_ear() -> Part:
    w_range = (Y_RAIL_HALF_SIZE, Y_TENSIONER_HALF_WIDTH)
    ear = block(
        (Y_RAIL_END_U - Y_EAR_LENGTH_ALONG_RAIL, Y_RAIL_END_U), w_range, (Y_RAIL_BOTTOM_V, Y_WHEEL_CLEARANCE_TOP_V)
    )
    countersink = Plane(
        origin=(Y_EAR_SCREW_U, Y_TENSIONER_HALF_WIDTH, Y_RAIL_SLOT_V), z_dir=(0, -1, 0)
    ).location * Cone(M4_COUNTERSINK_DIAMETER / 2, Y_EAR_SCREW_DIAMETER / 2, M4_COUNTERSINK_DEPTH, align=BOTTOM)
    return ear - hole_along_w(Y_EAR_SCREW_U, Y_RAIL_SLOT_V, Y_EAR_SCREW_DIAMETER, w_range) - countersink


def _y_bolt_access_slot() -> Part:
    reach = M5_HEAD_DIAMETER / 2 + BOLT_ACCESS_MARGIN
    return block(
        (Y_IDLER_TRAVEL[0] - reach, Y_IDLER_TRAVEL[1] + reach),
        (Y_RAIL_HALF_SIZE, Y_TENSIONER_HALF_WIDTH),
        (-reach, reach),
    )


def y_belt_tensioner_body() -> Part:
    end_wall = end_wall_u_range(Y_IDLER_TRAVEL)
    width = (-Y_TENSIONER_HALF_WIDTH, Y_TENSIONER_HALF_WIDTH)
    shell_u = (Y_RAIL_END_U, end_wall[1])
    shell_v = (Y_RAIL_BOTTOM_V, CASE_HALF_HEIGHT)
    body = case_channel(Y_RAIL_END_U, Y_IDLER_TRAVEL)
    body += block(shell_u, width, (-CASE_HALF_HEIGHT, -CASE_INNER_HALF_HEIGHT))
    body += block(shell_u, width, (CASE_INNER_HALF_HEIGHT, CASE_HALF_HEIGHT))
    body += block(end_wall, width, shell_v)
    side = block(shell_u, (Y_RAIL_HALF_SIZE, Y_TENSIONER_HALF_WIDTH), shell_v) + _y_ear()
    body += [side, mirror(side, Plane.XZ)]
    body -= stem_hole(Y_IDLER_TRAVEL)
    body -= _y_bolt_access_slot()
    body = Y_TENSIONER_LOCATION * body
    body.label = "y_belt_tensioner_body"
    body.color = PRINTED_PART_COLOR
    return body


def y_belt_tensioner_body_for_printing() -> Part:
    return resting_on_bed(PRINT_FROM_END_WALL * Y_TENSIONER_LOCATION.inverse() * y_belt_tensioner_body())
