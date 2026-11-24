from build123d import Part

from ender3_cad.ender3.reference.components.f688_bearing import f688_bearing
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.y_axis.dimensions import Y_FRONT_IDLER_RIGHT_BEARING_LOCATION


def y_front_idler_right_bearing() -> Part:
    return placed(f688_bearing(), Y_FRONT_IDLER_RIGHT_BEARING_LOCATION, "y_front_idler_right_bearing")
