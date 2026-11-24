from build123d import Cylinder, Keep, Part, Plane, Pos, Vector, mirror, split

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM, FACE_BACK, M3_CLEARANCE_DIAMETER
from ender3_cad.enclosure.dimensions import RAIL_END_Y, REAR_PANEL_Y_RANGE
from ender3_cad.ender3.reference.electronics.dimensions import (
    POWER_SUPPLY_BACK_TAPPED_HOLES,
    POWER_SUPPLY_FRONT_TAPPED_HOLES,
)
from ender3_cad.upgrades.board_cases.dimensions import RAIL_SLOT_CENTERS_Z, TRAY_BOTTOM_Z
from ender3_cad.upgrades.construction import t_rail
from ender3_cad.upgrades.power_supply_case.dimensions import (
    DRAWER_INNER_X,
    DRAWER_OUTER_X,
    PSU_CEILING_BOTTOM_Z,
    PSU_CEILING_TOP_Z,
    PSU_DEPTH,
    PSU_DRAWER_FRONT_Y,
    PSU_FRONT_Y,
    PSU_LOCATION,
    PSU_RIB_THICKNESS,
    PSU_X_RANGE,
)

LOWER_RAIL_SLOT_Z = RAIL_SLOT_CENTERS_Z[0]

SEAM_X = 0.0

PSU_RIB_WIDTH = 14.0
PSU_RIB_BELOW_HOLE = 6.0

PSU_CEILING_LIP = 7.0

PSU_Y_RANGE = (PSU_FRONT_Y, PSU_FRONT_Y + PSU_DEPTH)

PSU_FRONT_SCREWS = [(PSU_LOCATION * Pos(x, 0, z)).position for x, z in POWER_SUPPLY_FRONT_TAPPED_HOLES]
PSU_BACK_SCREWS = [(PSU_LOCATION * Pos(x, 0, z)).position for x, z in POWER_SUPPLY_BACK_TAPPED_HOLES]


def _psu_rib(screw: Vector, y_range: tuple[float, float]) -> Part:
    rib = block(
        (screw.X - PSU_RIB_WIDTH / 2, screw.X + PSU_RIB_WIDTH / 2),
        y_range,
        (screw.Z - PSU_RIB_BELOW_HOLE, PSU_CEILING_BOTTOM_Z),
    )
    return rib - Pos(screw.X, y_range[0], screw.Z) * FACE_BACK * Cylinder(
        M3_CLEARANCE_DIAMETER / 2, y_range[1] - y_range[0], align=BOTTOM
    )


def _drawer_body() -> Part:
    full_width = (-DRAWER_OUTER_X, DRAWER_OUTER_X)
    length = (PSU_DRAWER_FRONT_Y, REAR_PANEL_Y_RANGE[1])
    body = block(full_width, length, (PSU_CEILING_BOTTOM_Z, PSU_CEILING_TOP_Z))
    body -= block(
        (PSU_X_RANGE[0] + PSU_CEILING_LIP, PSU_X_RANGE[1] - PSU_CEILING_LIP),
        (PSU_Y_RANGE[0] + PSU_CEILING_LIP, PSU_Y_RANGE[1] - PSU_CEILING_LIP),
        (PSU_CEILING_BOTTOM_Z, PSU_CEILING_TOP_Z),
    )
    body += block(full_width, REAR_PANEL_Y_RANGE, (TRAY_BOTTOM_Z, PSU_CEILING_TOP_Z))
    side_wall = block((DRAWER_INNER_X, DRAWER_OUTER_X), length, (TRAY_BOTTOM_Z, PSU_CEILING_TOP_Z)) + t_rail(
        LOWER_RAIL_SLOT_Z, (PSU_DRAWER_FRONT_Y, RAIL_END_Y)
    )
    body += [side_wall, mirror(side_wall, Plane.YZ)]
    front_ribs = (PSU_Y_RANGE[0] - PSU_RIB_THICKNESS, PSU_Y_RANGE[0])
    back_ribs = (PSU_Y_RANGE[1], PSU_Y_RANGE[1] + PSU_RIB_THICKNESS)
    body += [_psu_rib(screw, front_ribs) for screw in PSU_FRONT_SCREWS]
    body += [_psu_rib(screw, back_ribs) for screw in PSU_BACK_SCREWS]
    return body


def power_supply_drawer_half(keep: Keep, label: str) -> Part:
    half = split(_drawer_body(), Plane.YZ.offset(SEAM_X), keep=keep)
    half.label = label
    half.color = PRINTED_PART_COLOR
    return half
