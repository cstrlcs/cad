from build123d import Part, Pos

from ender3.dimensions import FACE_BACK
from ender3.ender3.reference.components.fan_4010 import fan_4010
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.print_head.dimensions import (
    FAN_COVER_FAN_CENTER_X,
    FAN_COVER_FAN_CENTER_Z,
    FAN_COVER_LOCATION,
    FAN_COVER_SHEET_THICKNESS,
)

HOTEND_FAN_LOCATION = (
    FAN_COVER_LOCATION * Pos(FAN_COVER_FAN_CENTER_X, FAN_COVER_SHEET_THICKNESS, FAN_COVER_FAN_CENTER_Z) * FACE_BACK
)


def hotend_fan() -> Part:
    return placed(fan_4010(), HOTEND_FAN_LOCATION, "hotend_fan")
