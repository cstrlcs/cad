from build123d import Part, Rot, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3.enclosure.accessories.dimensions import LATCH_HEIGHT, MAGNET_POCKET_DEPTH, MAGNET_POCKET_DIAMETER
from ender3.enclosure.construction import blind_hole, latch_catch_screw_point
from ender3.enclosure.dimensions import (
    CASE_INNER_HALF_WIDTH,
    DOOR_HARDWARE_CENTER_Z,
    LATCH_CATCH_DEPTH,
    LATCH_CATCH_FRONT_Y,
    LATCH_CENTER_X,
    LATCH_FEATURE_OFFSET,
    LATCH_WIDTH,
)


def door_magnet_catch() -> Part:
    center_z = DOOR_HARDWARE_CENTER_Z
    catch = block(
        (LATCH_CENTER_X - LATCH_WIDTH / 2, CASE_INNER_HALF_WIDTH),
        (LATCH_CATCH_FRONT_Y, LATCH_CATCH_FRONT_Y + LATCH_CATCH_DEPTH),
        (center_z - LATCH_HEIGHT / 2, center_z + LATCH_HEIGHT / 2),
    )
    catch -= blind_hole(
        Vector(LATCH_CENTER_X, LATCH_CATCH_FRONT_Y, center_z + LATCH_FEATURE_OFFSET),
        Vector(0, 1, 0),
        MAGNET_POCKET_DIAMETER,
        MAGNET_POCKET_DEPTH,
    )
    catch -= blind_hole(
        latch_catch_screw_point(), Vector(-1, 0, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
    )
    catch.label = "door_magnet_catch"
    catch.color = PRINTED_PART_COLOR
    return catch


def door_magnet_catch_for_printing() -> Part:
    return resting_on_bed(Rot(90, 0, 0) * door_magnet_catch())
