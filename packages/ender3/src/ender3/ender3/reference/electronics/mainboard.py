from build123d import Cylinder, Part, Plane, Polygon, Pos, extrude

from ender3.construction import block
from ender3.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_BACK
from ender3.ender3.reference.electronics.construction import thin_plate_hole
from ender3.ender3.reference.electronics.dimensions import (
    MAINBOARD_LOCATION,
    MAINBOARD_MOUNTING_HOLES,
    MAINBOARD_PCB_THICKNESS,
    SD_CARD_SOCKET_ORIGIN,
    SD_CARD_SOCKET_SIZE,
    USB_SOCKET_ORIGIN,
    USB_SOCKET_SIZE,
)

MAINBOARD_PCB_SIZE = (70.0, 100.0)

MAINBOARD_MOUNTING_HOLE_DIAMETER = 3.5

CONNECTOR_SHELL_WALL = 0.5
FOUR_PIN_HEADER_SIZE = (6.0, 13.0, 9.0)
FOUR_PIN_HEADER_ORIGINS = [(1.0, 4.0), (1.0, 25.0), (1.0, 46.0), (1.0, 64.0)]
FOUR_PIN_HEADER_PIN_OFFSETS_Y = [2.6, 5.1, 7.6, 10.1]
FOUR_PIN_HEADER_PIN_X_RANGE = (3.0, 3.5)
FOUR_PIN_HEADER_PIN_HEIGHT = 7.5
TWO_PIN_HEADER_SIZE = (6.0, 8.0, 10.0)
TWO_PIN_HEADER_ORIGINS = [(55.0, 47.5)] + [(63.0, y) for y in (44.5, 53.0, 61.5, 70.0, 78.5, 87.0)]
TWO_PIN_HEADER_PIN_OFFSETS_Y = [2.4, 5.6]
TWO_PIN_HEADER_PIN_X_RANGE = (3.0, 3.5)
TWO_PIN_HEADER_PIN_HEIGHT = 8.5
HEADER_PIN_WIDTH = 0.7

SD_CARD_SOCKET_SLOT_X_RANGE = (3.0, 17.0)
SD_CARD_SOCKET_SLOT_START_Y = 85.5
SD_CARD_SOCKET_SLOT_Z_RANGE = (0.5, 1.0)

USB_SOCKET_CAVITY_X_RANGE = (22.8, 29.8)
USB_SOCKET_CAVITY_START_Y = 90.5
USB_SOCKET_CAVITY_Z_RANGE = (0.5, 3.1)
TEN_PIN_HEADER_ORIGIN = (42.5, 90.0)
TEN_PIN_HEADER_SIZE = (20.0, 10.0, 10.0)
TEN_PIN_HEADER_PIN_X = [46.75, 49.75, 52.75, 55.75, 58.75]
TEN_PIN_HEADER_PIN_Y = [93.4, 96.6]
TEN_PIN_HEADER_PIN_THICKNESS = 0.5
TEN_PIN_HEADER_PIN_HEIGHT = 8.594
POWER_TERMINAL_X_RANGE = (56.0, 70.0)
POWER_TERMINAL_FRONT_Y = 2.0
POWER_TERMINAL_PROFILE = [
    (POWER_TERMINAL_FRONT_Y, 0.0),
    (12.0, 0.0),
    (12.0, 18.3),
    (7.0, 18.3),
    (POWER_TERMINAL_FRONT_Y, 13.4714),
]
POWER_TERMINAL_WIRE_ENTRIES = [(60.071, 5.665, 2.348), (64.683, 5.665, 2.851)]
POWER_TERMINAL_WIRE_ENTRY_DEPTH = 5.0
HEATER_TERMINAL_ORIGIN = (60.0, 14.0)
HEATER_TERMINAL_SIZE = (10.0, 30.0, 15.0)
HEATER_TERMINAL_WIRE_ENTRY_SIZE = (2.0, 2.5, 2.5)
HEATER_TERMINAL_WIRE_ENTRY_Z = 2.5
HEATER_TERMINAL_WIRE_ENTRY_Y = [16.0, 20.0, 26.0, 30.0, 36.0, 40.0]


def _connector_shell(origin: tuple[float, float], size: tuple[float, float, float]) -> Part:
    (x, y), (dx, dy, dz), wall, z0 = origin, size, CONNECTOR_SHELL_WALL, MAINBOARD_PCB_THICKNESS
    shell = block((x, x + dx), (y, y + dy), (z0, z0 + dz))
    return shell - block((x + wall, x + dx - wall), (y + wall, y + dy - wall), (z0 + wall, z0 + dz + CUT_OVERSHOOT))


def mainboard() -> Part:
    t = MAINBOARD_PCB_THICKNESS
    wall = CONNECTOR_SHELL_WALL
    pcb_width, pcb_length = MAINBOARD_PCB_SIZE
    pcb = block((0, pcb_width), (0, pcb_length), (0, t)) - [
        Pos(x, y, 0) * thin_plate_hole(MAINBOARD_MOUNTING_HOLE_DIAMETER) for x, y in MAINBOARD_MOUNTING_HOLES
    ]
    four_pin_headers = [
        _connector_shell((x, y), FOUR_PIN_HEADER_SIZE)
        + [
            block(
                (x + FOUR_PIN_HEADER_PIN_X_RANGE[0], x + FOUR_PIN_HEADER_PIN_X_RANGE[1]),
                (y + dy - HEADER_PIN_WIDTH / 2, y + dy + HEADER_PIN_WIDTH / 2),
                (t + wall, t + wall + FOUR_PIN_HEADER_PIN_HEIGHT),
            )
            for dy in FOUR_PIN_HEADER_PIN_OFFSETS_Y
        ]
        for x, y in FOUR_PIN_HEADER_ORIGINS
    ]
    two_pin_headers = [
        _connector_shell((x, y), TWO_PIN_HEADER_SIZE)
        + [
            block(
                (x + TWO_PIN_HEADER_PIN_X_RANGE[0], x + TWO_PIN_HEADER_PIN_X_RANGE[1]),
                (y + dy - HEADER_PIN_WIDTH / 2, y + dy + HEADER_PIN_WIDTH / 2),
                (t + wall, t + wall + TWO_PIN_HEADER_PIN_HEIGHT),
            )
            for dy in TWO_PIN_HEADER_PIN_OFFSETS_Y
        ]
        for x, y in TWO_PIN_HEADER_ORIGINS
    ]
    (sx, sy), (sdx, sdy, sdz) = SD_CARD_SOCKET_ORIGIN, SD_CARD_SOCKET_SIZE
    sd_socket = block((sx, sx + sdx), (sy, sy + sdy), (t, t + sdz)) - block(
        SD_CARD_SOCKET_SLOT_X_RANGE,
        (SD_CARD_SOCKET_SLOT_START_Y, sy + sdy + CUT_OVERSHOOT),
        (t + SD_CARD_SOCKET_SLOT_Z_RANGE[0], t + SD_CARD_SOCKET_SLOT_Z_RANGE[1]),
    )
    (ux, uy), (udx, udy, udz) = USB_SOCKET_ORIGIN, USB_SOCKET_SIZE
    usb_socket = block((ux, ux + udx), (uy, uy + udy), (t, t + udz)) - block(
        USB_SOCKET_CAVITY_X_RANGE,
        (USB_SOCKET_CAVITY_START_Y, uy + udy + CUT_OVERSHOOT),
        (t + USB_SOCKET_CAVITY_Z_RANGE[0], t + USB_SOCKET_CAVITY_Z_RANGE[1]),
    )
    ten_pin_header = _connector_shell(TEN_PIN_HEADER_ORIGIN, TEN_PIN_HEADER_SIZE) + [
        block(
            (x - TEN_PIN_HEADER_PIN_THICKNESS / 2, x + TEN_PIN_HEADER_PIN_THICKNESS / 2),
            (y - HEADER_PIN_WIDTH / 2, y + HEADER_PIN_WIDTH / 2),
            (t + wall, t + wall + TEN_PIN_HEADER_PIN_HEIGHT),
        )
        for x in TEN_PIN_HEADER_PIN_X
        for y in TEN_PIN_HEADER_PIN_Y
    ]
    px0, px1 = POWER_TERMINAL_X_RANGE
    power_terminal = Pos(px0, 0, t) * extrude(Plane.YZ * Polygon(*POWER_TERMINAL_PROFILE, align=None), px1 - px0) - [
        Pos(x, POWER_TERMINAL_FRONT_Y, t + z)
        * FACE_BACK
        * Cylinder(d / 2, POWER_TERMINAL_WIRE_ENTRY_DEPTH, align=BOTTOM)
        for x, z, d in POWER_TERMINAL_WIRE_ENTRIES
    ]
    (hx, hy), (hdx, hdy, hdz) = HEATER_TERMINAL_ORIGIN, HEATER_TERMINAL_SIZE
    ex, ey, ez = HEATER_TERMINAL_WIRE_ENTRY_SIZE
    heater_terminal = block((hx, hx + hdx), (hy, hy + hdy), (t, t + hdz)) - [
        block(
            (hx + hdx - ex, hx + hdx + CUT_OVERSHOOT),
            (y, y + ey),
            (t + HEATER_TERMINAL_WIRE_ENTRY_Z, t + HEATER_TERMINAL_WIRE_ENTRY_Z + ez),
        )
        for y in HEATER_TERMINAL_WIRE_ENTRY_Y
    ]
    board = Part() + [
        pcb,
        *four_pin_headers,
        *two_pin_headers,
        sd_socket,
        usb_socket,
        ten_pin_header,
        power_terminal,
        heater_terminal,
    ]
    board = MAINBOARD_LOCATION * board
    board.label = "mainboard"
    return board
