from build123d import Part, Pos

from ender3_cad.dimensions import FACE_BACK
from ender3_cad.ender3.reference.components.wheel_spacer import wheel_spacer
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_BACK_Y,
    LEFT_PLATE_WHEEL_AXIS_X,
    UPPER_GANTRY_WHEEL_Z,
)

LEFT_PLATE_UPPER_WHEEL_PLATE_SPACER_LOCATION = (
    Pos(LEFT_PLATE_WHEEL_AXIS_X, GANTRY_PLATE_BACK_Y, UPPER_GANTRY_WHEEL_Z) * FACE_BACK
)


def left_plate_upper_wheel_plate_spacer() -> Part:
    return placed(wheel_spacer(), LEFT_PLATE_UPPER_WHEEL_PLATE_SPACER_LOCATION, "left_plate_upper_wheel_plate_spacer")
