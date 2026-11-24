from build123d import Part, Pos

from ender3_cad.dimensions import FACE_DOWN
from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.y_axis.dimensions import FRONT_LEFT_WHEEL_AXLE_POSITION, WHEEL_CENTER_Z

FRONT_LEFT_WHEEL_LOCATION = Pos(*FRONT_LEFT_WHEEL_AXLE_POSITION, WHEEL_CENTER_Z) * FACE_DOWN


def front_left_wheel() -> Part:
    return placed(v_wheel(), FRONT_LEFT_WHEEL_LOCATION, "front_left_wheel")
