from build123d import Part, Pos

from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.y_axis.dimensions import WHEEL_CENTER_Z

REAR_RIGHT_WHEEL_LOCATION = Pos(30.717849, -6.055359, WHEEL_CENTER_Z)


def rear_right_wheel() -> Part:
    return placed(v_wheel(), REAR_RIGHT_WHEEL_LOCATION, "rear_right_wheel")
