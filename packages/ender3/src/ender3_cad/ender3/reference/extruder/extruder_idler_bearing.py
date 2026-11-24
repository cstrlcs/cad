from build123d import Cylinder, Part, Pos, Torus

from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3_cad.ender3.reference.extruder.dimensions import EXTRUDER_MOUNT_LOCATION

IDLER_BEARING_POSITION = (-0.6893, -13.1363, 7.02)
IDLER_BEARING_OUTER_DIAMETER = 13.0
IDLER_BEARING_BORE_DIAMETER = 4.0
IDLER_BEARING_WIDTH = 4.0
IDLER_BEARING_GROOVE_RADIUS = 1.0


def extruder_idler_bearing() -> Part:
    bearing = Cylinder(IDLER_BEARING_OUTER_DIAMETER / 2, IDLER_BEARING_WIDTH, align=BOTTOM)
    bearing -= Cylinder(IDLER_BEARING_BORE_DIAMETER / 2, CUT_THROUGH_LENGTH)
    bearing -= Pos(0, 0, IDLER_BEARING_WIDTH / 2) * Torus(IDLER_BEARING_OUTER_DIAMETER / 2, IDLER_BEARING_GROOVE_RADIUS)
    bearing = EXTRUDER_MOUNT_LOCATION * Pos(*IDLER_BEARING_POSITION) * bearing
    bearing.label = "extruder_idler_bearing"
    return bearing
