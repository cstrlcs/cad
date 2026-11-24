from build123d import Part, Rot

from ender3_cad.ender3.reference.components.eccentric_spacer import eccentric_spacer
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.print_head.construction import on_hole_axis
from ender3_cad.ender3.reference.print_head.dimensions import WHEEL_SPACER_END_Y, X_CARRIAGE_PLATE_CENTER_HOLE_POINT

LOWER_ECCENTRIC_SPACER_LOCATION = on_hole_axis(X_CARRIAGE_PLATE_CENTER_HOLE_POINT, WHEEL_SPACER_END_Y) * Rot(
    90, 0, 52.878067
)


def lower_eccentric_spacer() -> Part:
    return placed(eccentric_spacer(), LOWER_ECCENTRIC_SPACER_LOCATION, "lower_eccentric_spacer")
