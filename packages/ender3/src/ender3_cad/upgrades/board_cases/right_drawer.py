from build123d import Part, Plane, Pos, mirror

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import (
    CUT_OVERSHOOT,
    FACE_DOWN,
    M2_5_HEAT_SET_INSERT_DEPTH,
    M2_5_HEAT_SET_INSERT_HOLE_DIAMETER,
    M3_HEAT_SET_INSERT_DEPTH,
    M3_HEAT_SET_INSERT_HOLE_DIAMETER,
)
from ender3_cad.ender3.purchased.lm2596_module import LM2596_MOUNTING_HOLES
from ender3_cad.ender3.purchased.raspberry_pi_3b import (
    RASPBERRY_PI_3B_AUDIO_Y,
    RASPBERRY_PI_3B_CAMERA_CONNECTOR_CENTER,
    RASPBERRY_PI_3B_ETHERNET_CENTER_Y,
    RASPBERRY_PI_3B_ETHERNET_HEIGHT,
    RASPBERRY_PI_3B_ETHERNET_WIDTH,
    RASPBERRY_PI_3B_MOUNTING_HOLES,
    RASPBERRY_PI_3B_PCB_THICKNESS,
    RASPBERRY_PI_3B_USB_CENTERS_Y,
    RASPBERRY_PI_3B_USB_HEIGHT,
    RASPBERRY_PI_3B_USB_WIDTH,
)
from ender3_cad.upgrades.board_cases.construction import front_port_cutouts, left_shell, standoffs_and_insert_holes
from ender3_cad.upgrades.board_cases.dimensions import (
    CEILING_BOTTOM_Z,
    CEILING_TOP_Z,
    DRAWER_BACK_Y,
    LM2596_LOCATION,
    LM2596_STANDOFF_HEIGHT,
    PI_BOARD_BACK_Z,
    PI_LOCATION,
    PI_POWER_EDGE_X,
    PORT_OPENING_MARGIN,
)

PI_COMPONENT_SIDE_Z = PI_BOARD_BACK_Z - RASPBERRY_PI_3B_PCB_THICKNESS

PI_STANDOFF_POINTS = [(PI_LOCATION * Pos(x, y, 0)).position for x, y in RASPBERRY_PI_3B_MOUNTING_HOLES]
CAMERA_RIBBON_SLOT_WIDTH = 1.5
CAMERA_RIBBON_SLOT_LENGTH = 22.0
CAMERA_RIBBON_SLOT_GAP = 1.0
CAMERA_RIBBON_SLOT_X = PI_POWER_EDGE_X - RASPBERRY_PI_3B_AUDIO_Y[0] + CAMERA_RIBBON_SLOT_GAP
CAMERA_RIBBON_SLOT_CENTER_Y = (PI_LOCATION * Pos(*RASPBERRY_PI_3B_CAMERA_CONNECTOR_CENTER, 0)).position.Y

PI_FRONT_PORTS = [
    (center_y, RASPBERRY_PI_3B_USB_WIDTH, RASPBERRY_PI_3B_USB_HEIGHT) for center_y in RASPBERRY_PI_3B_USB_CENTERS_Y
] + [(RASPBERRY_PI_3B_ETHERNET_CENTER_Y, RASPBERRY_PI_3B_ETHERNET_WIDTH, RASPBERRY_PI_3B_ETHERNET_HEIGHT)]
PI_FRONT_PORT_CENTERS_X = [(PI_LOCATION * Pos(0, center_y, 0)).position.X for center_y, _, _ in PI_FRONT_PORTS]
RIGHT_PORT_OPENINGS = [
    (
        (center_x - port_width / 2 - PORT_OPENING_MARGIN, center_x + port_width / 2 + PORT_OPENING_MARGIN),
        (PI_COMPONENT_SIDE_Z - port_height - PORT_OPENING_MARGIN, PI_COMPONENT_SIDE_Z + PORT_OPENING_MARGIN),
    )
    for center_x, (_, port_width, port_height) in zip(PI_FRONT_PORT_CENTERS_X, PI_FRONT_PORTS, strict=True)
]

LM2596_STANDOFF_POINTS = [(LM2596_LOCATION * Pos(x, y, 0)).position for x, y in LM2596_MOUNTING_HOLES]

SUPPLY_CABLE_NOTCH_X = (100.0, 112.0)
SUPPLY_CABLE_NOTCH_LENGTH = 8.0
SUPPLY_CABLE_NOTCH_BOTTOM_Z = 32.0


def right_drawer() -> Part:
    pi_standoffs, pi_insert_holes = standoffs_and_insert_holes(
        PI_STANDOFF_POINTS, M2_5_HEAT_SET_INSERT_HOLE_DIAMETER, M2_5_HEAT_SET_INSERT_DEPTH, PI_BOARD_BACK_Z
    )
    buck_standoffs, buck_insert_holes = standoffs_and_insert_holes(
        LM2596_STANDOFF_POINTS,
        M3_HEAT_SET_INSERT_HOLE_DIAMETER,
        M3_HEAT_SET_INSERT_DEPTH,
        CEILING_BOTTOM_Z - LM2596_STANDOFF_HEIGHT,
    )
    supply_cable_notch = block(
        SUPPLY_CABLE_NOTCH_X,
        (DRAWER_BACK_Y - SUPPLY_CABLE_NOTCH_LENGTH, DRAWER_BACK_Y + CUT_OVERSHOOT),
        (SUPPLY_CABLE_NOTCH_BOTTOM_Z, CEILING_TOP_Z + CUT_OVERSHOOT),
    )
    drawer = mirror(left_shell(), Plane.YZ) + pi_standoffs + buck_standoffs
    camera_ribbon_slot = block(
        (CAMERA_RIBBON_SLOT_X, CAMERA_RIBBON_SLOT_X + CAMERA_RIBBON_SLOT_WIDTH),
        (
            CAMERA_RIBBON_SLOT_CENTER_Y - CAMERA_RIBBON_SLOT_LENGTH / 2,
            CAMERA_RIBBON_SLOT_CENTER_Y + CAMERA_RIBBON_SLOT_LENGTH / 2,
        ),
        (CEILING_BOTTOM_Z - CUT_OVERSHOOT, CEILING_TOP_Z + CUT_OVERSHOOT),
    )
    drawer -= (
        pi_insert_holes
        + buck_insert_holes
        + front_port_cutouts(RIGHT_PORT_OPENINGS)
        + [supply_cable_notch, camera_ribbon_slot]
    )
    drawer.label = "right_drawer"
    drawer.color = PRINTED_PART_COLOR
    return drawer


def right_drawer_for_printing() -> Part:
    return resting_on_bed(FACE_DOWN * right_drawer())
