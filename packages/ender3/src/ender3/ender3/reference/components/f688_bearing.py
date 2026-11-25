from build123d import Axis, Cylinder, Part, SortBy, fillet

from ender3.dimensions import BOTTOM
from ender3.ender3.reference.components.dimensions import (
    F688_BORE_DIAMETER,
    F688_OUTER_DIAMETER,
    F688_WIDTH,
)

F688_FLANGE_DIAMETER = 18.0
F688_FLANGE_THICKNESS = 1.0
F688_OUTER_EDGE_ROUND = 0.5


def f688_bearing() -> Part:
    bearing = Cylinder(F688_FLANGE_DIAMETER / 2, F688_FLANGE_THICKNESS, align=BOTTOM) + Cylinder(
        F688_OUTER_DIAMETER / 2, F688_WIDTH, align=BOTTOM
    )
    bearing = fillet(bearing.edges().group_by(Axis.Z)[-1].sort_by(SortBy.RADIUS)[-1], F688_OUTER_EDGE_ROUND)
    bearing -= Cylinder(F688_BORE_DIAMETER / 2, F688_WIDTH, align=BOTTOM)
    bearing.label = "f688_bearing"
    return bearing
