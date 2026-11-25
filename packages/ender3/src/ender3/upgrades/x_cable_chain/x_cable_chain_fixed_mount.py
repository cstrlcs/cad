from build123d import Cylinder, Part, Pos, Rot, Vector, offset

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import BOTTOM, FACE_BACK, M5_CLEARANCE_DIAMETER
from ender3.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_FRAME,
    GANTRY_PLATE_FRONT_Y,
    GANTRY_PLATE_THICKNESS,
)
from ender3.ender3.reference.x_axis.left_gantry_plate import (
    LEFT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME,
    left_gantry_plate,
)
from ender3.upgrades.x_cable_chain.construction import chain_frame, female_end, stop_joints
from ender3.upgrades.x_cable_chain.dimensions import (
    CABLE_WINDOW_LENGTH,
    CHAIN_AXIS_Z,
    CHAIN_Z_RANGE,
    FIXED_MOUNT_PIVOT_X,
    FIXED_RUN_Y,
    LINK_HEIGHT,
    LINK_WIDTH,
    MOUNT_BODY_LENGTH,
    OUTER_ZONE_START_Y,
)

GANTRY_PAD_THICKNESS = 4.0
GANTRY_PAD_X_RANGE = (-189.5, -166.0)
GANTRY_PAD_Z_RANGE = (296.0, CHAIN_Z_RANGE[1])
GANTRY_HOOK_X_RANGE = (GANTRY_PAD_X_RANGE[0], -168.0)
GANTRY_HOOK_LIP_DEPTH = 2.0
GANTRY_HOOK_Z_RANGE = (309.0, 319.0)
GANTRY_FIT_CLEARANCE = 0.2
ZIP_TIE_SLOT_SIZE = (2.0, 4.0)
ZIP_TIE_SLOT_Y = (-62.0, -44.0)
ZIP_TIE_SLOT_INSET = 1.0
UPPER_WHEEL_HOLE = 1


def x_cable_chain_fixed_mount() -> Part:
    window_start = OUTER_ZONE_START_Y - CABLE_WINDOW_LENGTH
    half_width = LINK_WIDTH / 2
    chain_end = female_end(window_start) + stop_joints()
    chain_end += block((-half_width, half_width), (window_start - MOUNT_BODY_LENGTH, window_start), (0, LINK_HEIGHT))
    pivot = Vector(FIXED_MOUNT_PIVOT_X, FIXED_RUN_Y, CHAIN_AXIS_Z)
    mount = chain_frame(pivot, Vector(1, 0, 0)) * chain_end
    arm_x = (FIXED_MOUNT_PIVOT_X + window_start - MOUNT_BODY_LENGTH, FIXED_MOUNT_PIVOT_X + window_start)
    pad_front_y = GANTRY_PLATE_FRONT_Y - GANTRY_PAD_THICKNESS
    mount += block(arm_x, (FIXED_RUN_Y - LINK_HEIGHT / 2, pad_front_y), CHAIN_Z_RANGE)
    mount += block(GANTRY_PAD_X_RANGE, (pad_front_y, GANTRY_PLATE_FRONT_Y), GANTRY_PAD_Z_RANGE)
    plate_back_y = GANTRY_PLATE_FRONT_Y + GANTRY_PLATE_THICKNESS
    hook = block(GANTRY_HOOK_X_RANGE, (pad_front_y, plate_back_y + GANTRY_HOOK_LIP_DEPTH), GANTRY_HOOK_Z_RANGE)
    mount += hook - offset(left_gantry_plate(), GANTRY_FIT_CLEARANCE)
    wheel_hole = (GANTRY_PLATE_FRAME * Pos(*LEFT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME[UPPER_WHEEL_HOLE], 0)).position
    mount -= (
        Pos(wheel_hole.X, pad_front_y, wheel_hole.Z)
        * FACE_BACK
        * Cylinder(M5_CLEARANCE_DIAMETER / 2, GANTRY_PAD_THICKNESS, align=BOTTOM)
    )
    slot_x, slot_y = ZIP_TIE_SLOT_SIZE
    slot_x_range = (arm_x[1] - ZIP_TIE_SLOT_INSET - slot_x, arm_x[1] - ZIP_TIE_SLOT_INSET)
    mount -= [block(slot_x_range, (y - slot_y / 2, y + slot_y / 2), CHAIN_Z_RANGE) for y in ZIP_TIE_SLOT_Y]
    mount.label = "x_cable_chain_fixed_mount"
    mount.color = PRINTED_PART_COLOR
    return mount


def x_cable_chain_fixed_mount_for_printing() -> Part:
    return resting_on_bed(Rot(0, -90, 0) * x_cable_chain_fixed_mount())
