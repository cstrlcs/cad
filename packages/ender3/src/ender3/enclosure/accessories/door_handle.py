from build123d import Part, Rot, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3.enclosure.construction import blind_hole, handle_screw_points
from ender3.enclosure.dimensions import (
    DOOR_FRONT_Y,
    DOOR_HARDWARE_CENTER_Z,
    HANDLE_CENTER_X,
    HANDLE_LENGTH,
    HANDLE_POST_LENGTH,
    HANDLE_WIDTH,
)

HANDLE_DEPTH = 25.0

HANDLE_GRIP_THICKNESS = 8.0


def door_handle() -> Part:
    center_z = DOOR_HARDWARE_CENTER_Z
    x_range = (HANDLE_CENTER_X - HANDLE_WIDTH / 2, HANDLE_CENTER_X + HANDLE_WIDTH / 2)
    handle = block(
        x_range,
        (DOOR_FRONT_Y - HANDLE_DEPTH, DOOR_FRONT_Y),
        (center_z - HANDLE_LENGTH / 2, center_z + HANDLE_LENGTH / 2),
    )
    finger_reach = HANDLE_LENGTH / 2 - HANDLE_POST_LENGTH
    handle -= block(
        x_range,
        (DOOR_FRONT_Y - HANDLE_DEPTH + HANDLE_GRIP_THICKNESS, DOOR_FRONT_Y),
        (center_z - finger_reach, center_z + finger_reach),
    )
    handle -= [
        blind_hole(point, Vector(0, -1, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH)
        for point in handle_screw_points()
    ]
    handle.label = "door_handle"
    handle.color = PRINTED_PART_COLOR
    return handle


def door_handle_for_printing() -> Part:
    return resting_on_bed(Rot(0, 90, 0) * door_handle())
