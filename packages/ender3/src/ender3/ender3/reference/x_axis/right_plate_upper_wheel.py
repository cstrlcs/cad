from build123d import Part, Pos

from ender3.dimensions import FACE_BACK
from ender3.ender3.reference.components.v_wheel import v_wheel
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.x_axis.dimensions import (
    GANTRY_WHEEL_CENTER_Y,
    RIGHT_PLATE_WHEEL_AXIS_X,
    UPPER_GANTRY_WHEEL_Z,
)

RIGHT_PLATE_UPPER_WHEEL_LOCATION = (
    Pos(RIGHT_PLATE_WHEEL_AXIS_X, GANTRY_WHEEL_CENTER_Y, UPPER_GANTRY_WHEEL_Z) * FACE_BACK
)


def right_plate_upper_wheel() -> Part:
    return placed(v_wheel(), RIGHT_PLATE_UPPER_WHEEL_LOCATION, "right_plate_upper_wheel")
