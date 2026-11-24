from build123d import Part

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import resting_on_bed
from ender3_cad.upgrades.board_cases.construction import floor_tray
from ender3_cad.upgrades.board_cases.dimensions import (
    LEFT_FAN_CENTER,
    LEFT_INNER_X,
    LEFT_OUTER_X,
    LEFT_TRAY_SCREW_POINTS,
)


def left_floor_tray() -> Part:
    tray = floor_tray((LEFT_OUTER_X, LEFT_INNER_X), LEFT_TRAY_SCREW_POINTS, LEFT_FAN_CENTER)
    tray.label = "left_floor_tray"
    tray.color = PRINTED_PART_COLOR
    return tray


def left_floor_tray_for_printing() -> Part:
    return resting_on_bed(left_floor_tray())
