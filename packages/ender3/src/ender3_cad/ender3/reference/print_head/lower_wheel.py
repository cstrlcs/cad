from build123d import Part, Pos

from ender3_cad.dimensions import FACE_FRONT
from ender3_cad.ender3.reference.components.v_wheel import v_wheel
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.print_head.construction import on_hole_axis
from ender3_cad.ender3.reference.print_head.dimensions import WHEEL_CENTER_Y, X_CARRIAGE_PLATE_CENTER_HOLE_POINT

LOWER_WHEEL_ECCENTRIC_OFFSET = (-0.558148, 0.0, 0.422459)

LOWER_WHEEL_LOCATION = (
    Pos(*LOWER_WHEEL_ECCENTRIC_OFFSET) * on_hole_axis(X_CARRIAGE_PLATE_CENTER_HOLE_POINT, WHEEL_CENTER_Y) * FACE_FRONT
)


def lower_wheel() -> Part:
    return placed(v_wheel(), LOWER_WHEEL_LOCATION, "lower_wheel")
