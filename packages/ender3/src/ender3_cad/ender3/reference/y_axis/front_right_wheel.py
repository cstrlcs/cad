from build123d import Part, Pos

from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.y_axis.dimensions import WHEEL_CENTER_Z

FRONT_RIGHT_WHEEL_LOCATION = Pos(30.768787, -65.177691, WHEEL_CENTER_Z)


def front_right_wheel() -> Part:
    return placed(v_wheel(), FRONT_RIGHT_WHEEL_LOCATION, "front_right_wheel")
