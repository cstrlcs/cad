from build123d import Part, Pos

from ender3.dimensions import FACE_FRONT
from ender3.ender3.reference.components.v_wheel import v_wheel
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.x_axis.dimensions import (
    GANTRY_WHEEL_CENTER_Y,
    LEFT_PLATE_WHEEL_AXIS_X,
    UPPER_GANTRY_WHEEL_Z,
)

LEFT_PLATE_UPPER_WHEEL_LOCATION = Pos(LEFT_PLATE_WHEEL_AXIS_X, GANTRY_WHEEL_CENTER_Y, UPPER_GANTRY_WHEEL_Z) * FACE_FRONT


def left_plate_upper_wheel() -> Part:
    return placed(v_wheel(), LEFT_PLATE_UPPER_WHEEL_LOCATION, "left_plate_upper_wheel")
