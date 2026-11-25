from build123d import Part, Pos

from ender3.dimensions import FACE_BACK
from ender3.ender3.reference.components.wheel_spacer import wheel_spacer
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_BACK_Y,
    LOWER_GANTRY_WHEEL_Z,
    RIGHT_PLATE_WHEEL_AXIS_X,
)

RIGHT_PLATE_LOWER_WHEEL_PLATE_SPACER_LOCATION = (
    Pos(RIGHT_PLATE_WHEEL_AXIS_X, GANTRY_PLATE_BACK_Y, LOWER_GANTRY_WHEEL_Z) * FACE_BACK
)


def right_plate_lower_wheel_plate_spacer() -> Part:
    return placed(wheel_spacer(), RIGHT_PLATE_LOWER_WHEEL_PLATE_SPACER_LOCATION, "right_plate_lower_wheel_plate_spacer")
