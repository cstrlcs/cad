from build123d import Part

from ender3.dimensions import FACE_FRONT
from ender3.ender3.reference.components.wheel_spacer import wheel_spacer
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.print_head.construction import on_hole_axis
from ender3.ender3.reference.print_head.dimensions import WHEEL_SPACER_END_Y, X_CARRIAGE_PLATE_UPPER_LEFT_HOLE_POINT

UPPER_LEFT_WHEEL_SPACER_LOCATION = on_hole_axis(X_CARRIAGE_PLATE_UPPER_LEFT_HOLE_POINT, WHEEL_SPACER_END_Y) * FACE_FRONT


def upper_left_wheel_spacer() -> Part:
    return placed(wheel_spacer(), UPPER_LEFT_WHEEL_SPACER_LOCATION, "upper_left_wheel_spacer")
