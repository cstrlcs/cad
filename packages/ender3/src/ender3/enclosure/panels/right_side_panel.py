from build123d import Part, Vector

from ender3.dimensions import M3_CLEARANCE_DIAMETER
from ender3.enclosure.construction import camera_insert_points, hole, latch_catch_screw_point
from ender3.enclosure.panels.construction import side_panel


def right_side_panel() -> Part:
    screw_points = [latch_catch_screw_point(), *camera_insert_points()]
    return side_panel(1, [hole(point, Vector(1, 0, 0), M3_CLEARANCE_DIAMETER) for point in screw_points])
