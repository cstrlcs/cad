from build123d import Part, Pos

from ender3.dimensions import FACE_DOWN
from ender3.ender3.reference.components.v_wheel import v_wheel
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.y_axis.dimensions import REAR_LEFT_WHEEL_AXLE_POSITION, WHEEL_CENTER_Z

REAR_LEFT_WHEEL_LOCATION = Pos(*REAR_LEFT_WHEEL_AXLE_POSITION, WHEEL_CENTER_Z) * FACE_DOWN


def rear_left_wheel() -> Part:
    return placed(v_wheel(), REAR_LEFT_WHEEL_LOCATION, "rear_left_wheel")
