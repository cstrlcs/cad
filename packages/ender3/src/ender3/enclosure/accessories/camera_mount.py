from build123d import Part, Rot, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3.enclosure.construction import (
    blind_hole,
    camera_flange_ranges,
    camera_holder,
    camera_insert_points,
    camera_location,
)
from ender3.enclosure.dimensions import CAMERA_CLEARANCE, CASE_INNER_HALF_WIDTH, CUTTER_REACH
from ender3.ender3.purchased.raspberry_pi_camera_module import (
    RASPBERRY_PI_CAMERA_CONNECTOR_SIZE,
    RASPBERRY_PI_CAMERA_PCB_SIZE,
    RASPBERRY_PI_CAMERA_PCB_THICKNESS,
)

CAMERA_FLANGE_THICKNESS = M3_HEAT_SET_INSERT_DEPTH + 2.0


def _camera_insertion_opening() -> Part:
    width, height = RASPBERRY_PI_CAMERA_PCB_SIZE
    c = CAMERA_CLEARANCE
    return block((-c, width + c), (-c, height + c), (-CUTTER_REACH, 0))


def _camera_ribbon_exit() -> Part:
    width = RASPBERRY_PI_CAMERA_PCB_SIZE[0]
    c = CAMERA_CLEARANCE
    depth = RASPBERRY_PI_CAMERA_PCB_THICKNESS + RASPBERRY_PI_CAMERA_CONNECTOR_SIZE[2] + c
    half_width = RASPBERRY_PI_CAMERA_CONNECTOR_SIZE[0] / 2 + c
    return block((width / 2 - half_width, width / 2 + half_width), (-CUTTER_REACH, 0), (-depth, 0))


def camera_mount() -> Part:
    mount = camera_holder() + block(
        (CASE_INNER_HALF_WIDTH - CAMERA_FLANGE_THICKNESS, CASE_INNER_HALF_WIDTH), *camera_flange_ranges()
    )
    mount -= camera_location() * (_camera_insertion_opening() + _camera_ribbon_exit())
    mount -= [
        blind_hole(point, Vector(-1, 0, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH)
        for point in camera_insert_points()
    ]
    mount.label = "camera_mount"
    mount.color = PRINTED_PART_COLOR
    return mount


def camera_mount_for_printing() -> Part:
    return resting_on_bed(Rot(0, 90, 0) * camera_mount())
