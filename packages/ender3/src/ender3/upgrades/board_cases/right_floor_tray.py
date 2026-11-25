from build123d import Part

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import resting_on_bed
from ender3.upgrades.board_cases.construction import floor_tray
from ender3.upgrades.board_cases.dimensions import (
    LEFT_INNER_X,
    LEFT_OUTER_X,
    LEFT_TRAY_SCREW_POINTS,
    RIGHT_FAN_CENTER,
)

RIGHT_TRAY_SCREW_POINTS = [(-x, y) for x, y in LEFT_TRAY_SCREW_POINTS]


def right_floor_tray() -> Part:
    tray = floor_tray((-LEFT_INNER_X, -LEFT_OUTER_X), RIGHT_TRAY_SCREW_POINTS, RIGHT_FAN_CENTER)
    tray.label = "right_floor_tray"
    tray.color = PRINTED_PART_COLOR
    return tray


def right_floor_tray_for_printing() -> Part:
    return resting_on_bed(right_floor_tray())
