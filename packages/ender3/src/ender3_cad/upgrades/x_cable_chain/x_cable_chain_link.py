from build123d import Part, Pos

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block
from ender3_cad.upgrades.x_cable_chain.construction import female_end, male_end, mirrored_x_ranges, stop_joints
from ender3_cad.upgrades.x_cable_chain.dimensions import (
    COVER_BARB_DEPTH,
    COVER_BARB_Z,
    COVER_LEG_Y_RANGE,
    INNER_PLATE_X,
    INNER_ZONE_END_Y,
    LINK_PITCH,
    OUTER_ZONE_START_Y,
)

FLOOR_OVERHANG_PAST_PIVOT = 4.0
FLOOR_Y_RANGE = (-LINK_PITCH - FLOOR_OVERHANG_PAST_PIVOT, OUTER_ZONE_START_Y)
FLOOR_THICKNESS = 1.6
COVER_GROOVE_DEPTH = 0.45
COVER_GROOVE_CLEARANCE = 0.15


def x_cable_chain_link() -> Part:
    floor = block((-INNER_PLATE_X, INNER_PLATE_X), FLOOR_Y_RANGE, (0, FLOOR_THICKNESS))
    link = female_end(OUTER_ZONE_START_Y) + Pos(0, -LINK_PITCH, 0) * male_end(INNER_ZONE_END_Y + LINK_PITCH)
    groove_y = (COVER_LEG_Y_RANGE[0] - COVER_GROOVE_CLEARANCE, COVER_LEG_Y_RANGE[1] + COVER_GROOVE_CLEARANCE)
    groove_z = (COVER_BARB_Z - COVER_GROOVE_CLEARANCE, COVER_BARB_Z + 2 * COVER_BARB_DEPTH + COVER_GROOVE_CLEARANCE)
    grooves = [block(x_range, groove_y, groove_z) for x_range in mirrored_x_ranges(INNER_PLATE_X, COVER_GROOVE_DEPTH)]
    link += [*stop_joints(), floor]
    link -= grooves
    link.label = "x_cable_chain_link"
    link.color = PRINTED_PART_COLOR
    return link
