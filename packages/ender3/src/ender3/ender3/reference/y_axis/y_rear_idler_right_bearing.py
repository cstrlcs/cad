from build123d import Part, Pos

from ender3.dimensions import FACE_LEFT
from ender3.ender3.reference.components.f688_bearing import f688_bearing
from ender3.ender3.reference.construction import placed

Y_REAR_IDLER_RIGHT_BEARING_LOCATION = Pos(5.0, 140.0, 68.0) * FACE_LEFT


def y_rear_idler_right_bearing() -> Part:
    return placed(f688_bearing(), Y_REAR_IDLER_RIGHT_BEARING_LOCATION, "y_rear_idler_right_bearing")
