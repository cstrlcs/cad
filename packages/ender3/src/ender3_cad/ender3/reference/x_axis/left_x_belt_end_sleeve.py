from build123d import Location, Part

from ender3_cad.ender3.reference.components.belt_end_sleeve import belt_end_sleeve
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import X_BELT_END_SLEEVE_TILT_ABOUT_Y

LEFT_X_BELT_END_SLEEVE_LOCATION = Location((7.096796, -35.486433, 248.171302), (0, X_BELT_END_SLEEVE_TILT_ABOUT_Y, 0))


def left_x_belt_end_sleeve() -> Part:
    return placed(belt_end_sleeve(), LEFT_X_BELT_END_SLEEVE_LOCATION, "left_x_belt_end_sleeve")
