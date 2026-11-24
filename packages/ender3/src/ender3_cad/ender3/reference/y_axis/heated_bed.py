from build123d import Box, Cone, Cylinder, Part, Pos, RectangleRounded, extrude

from ender3_cad.dimensions import BOTTOM, TOP
from ender3_cad.ender3.reference.y_axis.dimensions import (
    BED_BOTTOM_Z,
    BED_CENTER_X,
    BED_CENTER_Y,
    BED_HEATER_PAD_POCKET_CENTER,
    BED_LEVELING_HOLE_OFFSETS,
    BED_SIZE,
    BED_THICKNESS,
)

BED_CORNER_RADIUS = 3.0

BED_LEVELING_HOLE_DIAMETER = 4.2
BED_LEVELING_HOLE_COUNTERSINK_DIAMETER = 9.8

BED_HEATER_PAD_POCKET_SIZE = (28.81216425, 11.44920980)
BED_HEATER_PAD_POCKET_DEPTH = 0.5
BED_LOCATION = Pos(BED_CENTER_X, BED_CENTER_Y, BED_BOTTOM_Z)


def heated_bed() -> Part:
    countersink_depth = (BED_LEVELING_HOLE_COUNTERSINK_DIAMETER - BED_LEVELING_HOLE_DIAMETER) / 2
    slab = extrude(RectangleRounded(*BED_SIZE, BED_CORNER_RADIUS), BED_THICKNESS)
    leveling_holes = [
        Pos(x, y, 0) * Cylinder(BED_LEVELING_HOLE_DIAMETER / 2, BED_THICKNESS, align=BOTTOM)
        + Pos(x, y, BED_THICKNESS)
        * Cone(
            BED_LEVELING_HOLE_DIAMETER / 2,
            BED_LEVELING_HOLE_COUNTERSINK_DIAMETER / 2,
            countersink_depth,
            align=TOP,
        )
        for x, y in BED_LEVELING_HOLE_OFFSETS
    ]
    heater_pad_pocket = Pos(*BED_HEATER_PAD_POCKET_CENTER, 0) * Box(
        *BED_HEATER_PAD_POCKET_SIZE, BED_HEATER_PAD_POCKET_DEPTH, align=BOTTOM
    )
    bed = BED_LOCATION * (slab - leveling_holes - heater_pad_pocket)
    bed.label = "heated_bed"
    return bed
