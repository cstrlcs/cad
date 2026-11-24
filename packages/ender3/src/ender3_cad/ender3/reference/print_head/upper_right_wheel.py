from build123d import Part

from ender3_cad.dimensions import FACE_FRONT
from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.print_head.construction import on_hole_axis
from ender3_cad.ender3.reference.print_head.dimensions import WHEEL_CENTER_Y, X_CARRIAGE_PLATE_UPPER_RIGHT_HOLE_POINT

UPPER_RIGHT_WHEEL_LOCATION = on_hole_axis(X_CARRIAGE_PLATE_UPPER_RIGHT_HOLE_POINT, WHEEL_CENTER_Y) * FACE_FRONT


def upper_right_wheel() -> Part:
    return placed(v_wheel(), UPPER_RIGHT_WHEEL_LOCATION, "upper_right_wheel")
