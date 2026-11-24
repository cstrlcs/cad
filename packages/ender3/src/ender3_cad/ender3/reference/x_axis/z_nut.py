from build123d import Cylinder, Part, Pos, Rectangle, Sketch, extrude

from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.reference.construction import circles
from ender3_cad.ender3.reference.z_axis.dimensions import LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y

Z_NUT_LOCATION = Pos(LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y, 304.0688)
Z_NUT_BORE_DIAMETER = 8.0
Z_NUT_PILOT_DIAMETER = 10.0
Z_NUT_PILOT_HEIGHT = 2.0
Z_NUT_FLANGE_RADIUS = 12.0
Z_NUT_FLANGE_ARC_OFFSET = 1.5
Z_NUT_FLANGE_FLAT_WIDTH = 12.6
Z_NUT_FLANGE_THICKNESS = 3.5
Z_NUT_FLANGE_HOLE_DIAMETER = 3.0
Z_NUT_FLANGE_HOLES_FROM_AXIS = [(0.0, -9.0), (0.0, 9.0)]
Z_NUT_BODY_DIAMETER = 10.2
Z_NUT_BODY_HEIGHT = 5.0


def z_nut() -> Part:
    flange = (
        Sketch() + circles([(0.0, -Z_NUT_FLANGE_ARC_OFFSET), (0.0, Z_NUT_FLANGE_ARC_OFFSET)], 2 * Z_NUT_FLANGE_RADIUS)
        & Rectangle(Z_NUT_FLANGE_FLAT_WIDTH, 4 * Z_NUT_FLANGE_RADIUS)
    ) - circles(Z_NUT_FLANGE_HOLES_FROM_AXIS, Z_NUT_FLANGE_HOLE_DIAMETER)
    total_height = Z_NUT_PILOT_HEIGHT + Z_NUT_FLANGE_THICKNESS + Z_NUT_BODY_HEIGHT
    nut = Z_NUT_LOCATION * (
        Cylinder(Z_NUT_PILOT_DIAMETER / 2, Z_NUT_PILOT_HEIGHT, align=BOTTOM)
        + Pos(0, 0, Z_NUT_PILOT_HEIGHT) * extrude(flange, Z_NUT_FLANGE_THICKNESS)
        + Pos(0, 0, Z_NUT_PILOT_HEIGHT + Z_NUT_FLANGE_THICKNESS)
        * Cylinder(Z_NUT_BODY_DIAMETER / 2, Z_NUT_BODY_HEIGHT, align=BOTTOM)
        - Cylinder(Z_NUT_BORE_DIAMETER / 2, total_height, align=BOTTOM)
    )
    nut.label = "z_nut"
    return nut
