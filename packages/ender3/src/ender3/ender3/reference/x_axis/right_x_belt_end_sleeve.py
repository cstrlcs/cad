from build123d import Location, Part

from ender3.ender3.reference.components.belt_end_sleeve import belt_end_sleeve
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.x_axis.dimensions import X_BELT_END_SLEEVE_TILT_ABOUT_Y

RIGHT_X_BELT_END_SLEEVE_LOCATION = Location((49.713703, -35.486433, 248.371521), (0, X_BELT_END_SLEEVE_TILT_ABOUT_Y, 0))


def right_x_belt_end_sleeve() -> Part:
    return placed(belt_end_sleeve(), RIGHT_X_BELT_END_SLEEVE_LOCATION, "right_x_belt_end_sleeve")
