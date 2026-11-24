from build123d import Part, Pos

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import (
    CUT_OVERSHOOT,
    FACE_DOWN,
    M3_HEAT_SET_INSERT_DEPTH,
    M3_HEAT_SET_INSERT_HOLE_DIAMETER,
)
from ender3_cad.ender3.reference.electronics.dimensions import (
    MAINBOARD_LOCATION,
    MAINBOARD_MOUNTING_HOLES,
    MAINBOARD_PCB_THICKNESS,
    SD_CARD_SOCKET_ORIGIN,
    SD_CARD_SOCKET_SIZE,
    USB_SOCKET_ORIGIN,
    USB_SOCKET_SIZE,
)
from ender3_cad.ender3.reference.frame.dimensions import (
    CROSS_MEMBER_ENCLOSURE_NOTCH_HEIGHT,
    CROSS_MEMBER_ENCLOSURE_NOTCH_X_RANGE,
)
from ender3_cad.upgrades.board_cases.construction import front_port_cutouts, left_shell, standoffs_and_insert_holes
from ender3_cad.upgrades.board_cases.dimensions import (
    DRAWER_BACK_Y,
    PORT_OPENING_MARGIN,
    TRAY_TOP_Z,
    WALL_THICKNESS,
)

MAINBOARD_BACK_Z = MAINBOARD_LOCATION.position.Z
MAINBOARD_COMPONENT_SIDE_Z = MAINBOARD_BACK_Z - MAINBOARD_PCB_THICKNESS
MAINBOARD_STANDOFF_POINTS = [(MAINBOARD_LOCATION * Pos(x, y, 0)).position for x, y in MAINBOARD_MOUNTING_HOLES]
LEFT_PORT_OPENINGS = [
    (
        (
            MAINBOARD_LOCATION.position.X + socket_x - PORT_OPENING_MARGIN,
            MAINBOARD_LOCATION.position.X + socket_x + socket_width + PORT_OPENING_MARGIN,
        ),
        (
            MAINBOARD_COMPONENT_SIDE_Z - socket_height - PORT_OPENING_MARGIN,
            MAINBOARD_COMPONENT_SIDE_Z + PORT_OPENING_MARGIN,
        ),
    )
    for (socket_x, _), (socket_width, _, socket_height) in (
        (SD_CARD_SOCKET_ORIGIN, SD_CARD_SOCKET_SIZE),
        (USB_SOCKET_ORIGIN, USB_SOCKET_SIZE),
    )
]


def left_drawer() -> Part:
    standoffs, insert_holes = standoffs_and_insert_holes(
        MAINBOARD_STANDOFF_POINTS, M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH, MAINBOARD_BACK_Z
    )
    harness_window = block(
        CROSS_MEMBER_ENCLOSURE_NOTCH_X_RANGE,
        (DRAWER_BACK_Y - WALL_THICKNESS - CUT_OVERSHOOT, DRAWER_BACK_Y + CUT_OVERSHOOT),
        (TRAY_TOP_Z - CUT_OVERSHOOT, CROSS_MEMBER_ENCLOSURE_NOTCH_HEIGHT),
    )
    drawer = left_shell() + standoffs - insert_holes - front_port_cutouts(LEFT_PORT_OPENINGS) - harness_window
    drawer.label = "left_drawer"
    drawer.color = PRINTED_PART_COLOR
    return drawer


def left_drawer_for_printing() -> Part:
    return resting_on_bed(FACE_DOWN * left_drawer())
