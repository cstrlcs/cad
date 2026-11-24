from build123d import Part, Plane, Polygon, Pos, extrude, mirror

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import FACE_DOWN
from ender3_cad.upgrades.x_cable_chain.dimensions import (
    COVER_BARB_DEPTH,
    COVER_BARB_Z,
    COVER_BOTTOM_Z,
    COVER_LEG_Y_RANGE,
    INNER_PLATE_X,
    LINK_HEIGHT,
    LINK_PITCH,
    PIVOT_Z,
)

COVER_STOP_GAP = 0.6
COVER_SIDE_CLEARANCE = 0.2
COVER_LEG_THICKNESS = 0.8
COVER_Y_RANGE = (-LINK_PITCH - PIVOT_Z + COVER_STOP_GAP / 2, -PIVOT_Z - COVER_STOP_GAP / 2)


def x_cable_chain_link_cover() -> Part:
    half_width = INNER_PLATE_X - COVER_SIDE_CLEARANCE
    bar = block((-half_width, half_width), COVER_Y_RANGE, (COVER_BOTTOM_Z, LINK_HEIGHT))
    leg = block(
        (INNER_PLATE_X - COVER_LEG_THICKNESS, INNER_PLATE_X),
        COVER_LEG_Y_RANGE,
        (COVER_BARB_Z, COVER_BOTTOM_Z),
    )
    barb_profile = Polygon(
        (INNER_PLATE_X, COVER_BARB_Z),
        (INNER_PLATE_X + COVER_BARB_DEPTH, COVER_BARB_Z + COVER_BARB_DEPTH),
        (INNER_PLATE_X, COVER_BARB_Z + 2 * COVER_BARB_DEPTH),
        align=None,
    )
    y0, y1 = COVER_LEG_Y_RANGE
    barb = Pos(0, y1, 0) * extrude(Plane.XZ * barb_profile, y1 - y0)
    side = leg + barb
    cover = bar + side + mirror(side, Plane.YZ)
    cover.label = "x_cable_chain_link_cover"
    cover.color = PRINTED_PART_COLOR
    return cover


def x_cable_chain_link_cover_for_printing() -> Part:
    return resting_on_bed(FACE_DOWN * x_cable_chain_link_cover())
