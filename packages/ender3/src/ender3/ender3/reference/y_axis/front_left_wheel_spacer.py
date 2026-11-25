from build123d import Part, Pos

from ender3.dimensions import FACE_DOWN
from ender3.ender3.reference.components.wheel_spacer import wheel_spacer
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.y_axis.dimensions import BED_CARRIAGE_PLATE_BOTTOM_Z, FRONT_LEFT_WHEEL_AXLE_POSITION

FRONT_LEFT_WHEEL_SPACER_LOCATION = Pos(*FRONT_LEFT_WHEEL_AXLE_POSITION, BED_CARRIAGE_PLATE_BOTTOM_Z) * FACE_DOWN


def front_left_wheel_spacer() -> Part:
    return placed(wheel_spacer(), FRONT_LEFT_WHEEL_SPACER_LOCATION, "front_left_wheel_spacer")
