from build123d import Part, Pos

from ender3_cad.dimensions import FACE_BACK
from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import (
    GANTRY_WHEEL_CENTER_Y,
    LOWER_GANTRY_WHEEL_Z,
    RIGHT_PLATE_WHEEL_AXIS_X,
)

RIGHT_PLATE_LOWER_WHEEL_LOCATION = (
    Pos(RIGHT_PLATE_WHEEL_AXIS_X, GANTRY_WHEEL_CENTER_Y, LOWER_GANTRY_WHEEL_Z) * FACE_BACK
)


def right_plate_lower_wheel() -> Part:
    return placed(v_wheel(), RIGHT_PLATE_LOWER_WHEEL_LOCATION, "right_plate_lower_wheel")
