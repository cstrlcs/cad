from build123d import Part, Pos

from ender3_cad.dimensions import FACE_BACK
from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import (
    GANTRY_WHEEL_CENTER_Y,
    LEFT_PLATE_ECCENTRIC_WHEEL_AXIS_X,
    LEFT_PLATE_ECCENTRIC_WHEEL_AXIS_Z,
)

LEFT_PLATE_ECCENTRIC_WHEEL_LOCATION = (
    Pos(LEFT_PLATE_ECCENTRIC_WHEEL_AXIS_X, GANTRY_WHEEL_CENTER_Y, LEFT_PLATE_ECCENTRIC_WHEEL_AXIS_Z) * FACE_BACK
)


def left_plate_eccentric_wheel() -> Part:
    return placed(v_wheel(), LEFT_PLATE_ECCENTRIC_WHEEL_LOCATION, "left_plate_eccentric_wheel")
