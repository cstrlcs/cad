from build123d import Part

from ender3_cad.ender3.reference.components.f688_bearing import f688_bearing
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import X_IDLER_BACK_BEARING_LOCATION


def x_idler_back_bearing() -> Part:
    return placed(f688_bearing(), X_IDLER_BACK_BEARING_LOCATION, "x_idler_back_bearing")
