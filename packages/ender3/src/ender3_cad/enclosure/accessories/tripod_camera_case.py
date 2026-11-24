from build123d import Cone, Cylinder, Part, Plane, Pos, Vector

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM, M2_PILOT_DIAMETER
from ender3_cad.enclosure.construction import blind_hole
from ender3_cad.enclosure.dimensions import CAMERA_CLEARANCE
from ender3_cad.ender3.purchased.raspberry_pi_camera_module import (
    RASPBERRY_PI_CAMERA_BLOCK_SIZE,
    RASPBERRY_PI_CAMERA_CONNECTOR_SIZE,
    RASPBERRY_PI_CAMERA_LENS_CENTER,
    RASPBERRY_PI_CAMERA_MOUNTING_HOLES,
    RASPBERRY_PI_CAMERA_PCB_SIZE,
    RASPBERRY_PI_CAMERA_PCB_THICKNESS,
)

TRIPOD_CASE_WALL_THICKNESS = 2.0
TRIPOD_CASE_FLOOR_THICKNESS = 2.0
PCB_POCKET_CLEARANCE = 0.3
LENS_BLOCK_CLEARANCE = 0.25
LENS_WINDOW_DIAMETER = 7.0
STANDOFF_DIAMETER = 4.6
STANDOFF_PILOT_FLOOR = 0.5
RIBBON_SLOT_WIDTH = 18.0

TRIPOD_BLOCK_DEPTH = 12.0
TRIPOD_BLOCK_HEIGHT = 18.0
TRIPOD_SELF_TAP_DIAMETER = 5.2
TRIPOD_SELF_TAP_DEPTH = 10.0
TRIPOD_ENTRY_CHAMFER = 0.8


def tripod_camera_case() -> Part:
    pcb_width, pcb_height = RASPBERRY_PI_CAMERA_PCB_SIZE
    pocket_x = pcb_width / 2 + PCB_POCKET_CLEARANCE
    pocket_y = pcb_height / 2 + PCB_POCKET_CLEARANCE
    outer_x = (-pocket_x - TRIPOD_CASE_WALL_THICKNESS, pocket_x + TRIPOD_CASE_WALL_THICKNESS)
    front_y = -pocket_y - TRIPOD_CASE_WALL_THICKNESS
    block_front_y = pocket_y + TRIPOD_CASE_WALL_THICKNESS
    back_y = block_front_y + TRIPOD_BLOCK_DEPTH
    standoff_top_z = TRIPOD_CASE_FLOOR_THICKNESS + RASPBERRY_PI_CAMERA_BLOCK_SIZE[2] + LENS_BLOCK_CLEARANCE
    pcb_back_z = standoff_top_z + RASPBERRY_PI_CAMERA_PCB_THICKNESS
    wall_top_z = pcb_back_z + RASPBERRY_PI_CAMERA_CONNECTOR_SIZE[2] + CAMERA_CLEARANCE
    pcb_frame = Pos(-pcb_width / 2, -pcb_height / 2)
    lens_x, lens_y = RASPBERRY_PI_CAMERA_LENS_CENTER

    case = block(outer_x, (front_y, block_front_y), (0, wall_top_z))
    case += block(outer_x, (block_front_y, back_y), (0, TRIPOD_BLOCK_HEIGHT))
    case -= block((-pocket_x, pocket_x), (-pocket_y, pocket_y), (TRIPOD_CASE_FLOOR_THICKNESS, wall_top_z))
    case += pcb_frame * [
        Pos(x, y, TRIPOD_CASE_FLOOR_THICKNESS)
        * Cylinder(STANDOFF_DIAMETER / 2, standoff_top_z - TRIPOD_CASE_FLOOR_THICKNESS, align=BOTTOM)
        for x, y in RASPBERRY_PI_CAMERA_MOUNTING_HOLES
    ]
    case -= pcb_frame * [
        blind_hole(
            Vector(x, y, standoff_top_z), Vector(0, 0, -1), M2_PILOT_DIAMETER, standoff_top_z - STANDOFF_PILOT_FLOOR
        )
        for x, y in RASPBERRY_PI_CAMERA_MOUNTING_HOLES
    ]
    case -= pcb_frame * blind_hole(
        Vector(lens_x, lens_y, 0), Vector(0, 0, 1), LENS_WINDOW_DIAMETER, TRIPOD_CASE_FLOOR_THICKNESS
    )
    case -= block((-RIBBON_SLOT_WIDTH / 2, RIBBON_SLOT_WIDTH / 2), (front_y, -pocket_y), (pcb_back_z, wall_top_z))
    tripod_entry = Vector(0, back_y, TRIPOD_BLOCK_HEIGHT / 2)
    case -= blind_hole(tripod_entry, Vector(0, -1, 0), TRIPOD_SELF_TAP_DIAMETER, TRIPOD_SELF_TAP_DEPTH)
    case -= Plane(origin=tripod_entry, z_dir=(0, -1, 0)).location * Cone(
        TRIPOD_SELF_TAP_DIAMETER / 2 + TRIPOD_ENTRY_CHAMFER,
        TRIPOD_SELF_TAP_DIAMETER / 2,
        TRIPOD_ENTRY_CHAMFER,
        align=BOTTOM,
    )
    case.label = "tripod_camera_case"
    case.color = PRINTED_PART_COLOR
    return case
