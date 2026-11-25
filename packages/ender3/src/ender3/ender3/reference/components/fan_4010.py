from build123d import Axis, Cylinder, Part, Pos, RectangleRounded, Rot, extrude, fillet

from ender3.construction import block
from ender3.dimensions import BOTTOM
from ender3.ender3.reference.components.dimensions import (
    FAN_4010_BORE_DIAMETER,
    FAN_4010_MOUNTING_HOLES,
    FAN_4010_SIZE,
    FAN_4010_THICKNESS,
)

FAN_4010_CORNER_RADIUS = 3.0

FAN_4010_HOLE_DIAMETER = 3.2
FAN_4010_COUNTERBORE_DIAMETER = 6.0
FAN_4010_COUNTERBORE_DEPTH = 4.0

FAN_4010_HUB_DIAMETER = 22.0
FAN_4010_HUB_INTAKE_EDGE_ROUND = 0.6
FAN_4010_STRUT_X_RANGE = (-10.532, -8.032)
FAN_4010_STRUT_THICKNESS = 1.5
FAN_4010_STRUT_ANGLES = (0.0, 120.0, 240.0)


def fan_4010() -> Part:
    frame = extrude(RectangleRounded(FAN_4010_SIZE, FAN_4010_SIZE, FAN_4010_CORNER_RADIUS), FAN_4010_THICKNESS)
    frame -= Cylinder(FAN_4010_BORE_DIAMETER / 2, FAN_4010_THICKNESS, align=BOTTOM)
    for x, y in FAN_4010_MOUNTING_HOLES:
        frame -= Pos(x, y, 0) * Cylinder(FAN_4010_HOLE_DIAMETER / 2, FAN_4010_THICKNESS, align=BOTTOM)
        frame -= Pos(x, y, 0) * Cylinder(FAN_4010_COUNTERBORE_DIAMETER / 2, FAN_4010_COUNTERBORE_DEPTH, align=BOTTOM)
    strut = block(
        FAN_4010_STRUT_X_RANGE,
        (-FAN_4010_BORE_DIAMETER / 2, 0),
        (FAN_4010_THICKNESS - FAN_4010_STRUT_THICKNESS, FAN_4010_THICKNESS),
    ) & Cylinder(FAN_4010_BORE_DIAMETER / 2, FAN_4010_THICKNESS, align=BOTTOM)
    hub = Cylinder(FAN_4010_HUB_DIAMETER / 2, FAN_4010_THICKNESS, align=BOTTOM)
    fan = frame + fillet(hub.edges().sort_by(Axis.Z)[0], FAN_4010_HUB_INTAKE_EDGE_ROUND)
    for angle in FAN_4010_STRUT_ANGLES:
        fan += Rot(0, 0, angle) * strut
    fan.label = "fan_4010"
    return fan
