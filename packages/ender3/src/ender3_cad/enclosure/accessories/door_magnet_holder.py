from build123d import Part, Rot, Vector

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3_cad.enclosure.accessories.dimensions import LATCH_HEIGHT, MAGNET_POCKET_DEPTH, MAGNET_POCKET_DIAMETER
from ender3_cad.enclosure.construction import blind_hole, latch_holder_screw_point
from ender3_cad.enclosure.dimensions import (
    DOOR_BACK_Y,
    DOOR_HARDWARE_CENTER_Z,
    LATCH_CENTER_X,
    LATCH_FEATURE_OFFSET,
    LATCH_HOLDER_THICKNESS,
    LATCH_WIDTH,
)


def door_magnet_holder() -> Part:
    center_z = DOOR_HARDWARE_CENTER_Z
    holder = block(
        (LATCH_CENTER_X - LATCH_WIDTH / 2, LATCH_CENTER_X + LATCH_WIDTH / 2),
        (DOOR_BACK_Y, DOOR_BACK_Y + LATCH_HOLDER_THICKNESS),
        (center_z - LATCH_HEIGHT / 2, center_z + LATCH_HEIGHT / 2),
    )
    holder -= blind_hole(
        Vector(LATCH_CENTER_X, DOOR_BACK_Y + LATCH_HOLDER_THICKNESS, center_z + LATCH_FEATURE_OFFSET),
        Vector(0, -1, 0),
        MAGNET_POCKET_DIAMETER,
        MAGNET_POCKET_DEPTH,
    )
    holder -= blind_hole(
        latch_holder_screw_point(), Vector(0, 1, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
    )
    holder.label = "door_magnet_holder"
    holder.color = PRINTED_PART_COLOR
    return holder


def door_magnet_holder_for_printing() -> Part:
    return resting_on_bed(Rot(-90, 0, 0) * door_magnet_holder())
