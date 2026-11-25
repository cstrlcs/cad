from build123d import Cylinder, Part, Pos

from ender3.dimensions import BOTTOM
from ender3.ender3.reference.z_axis.dimensions import LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y

LEAD_SCREW_DIAMETER = 8.0
LEAD_SCREW_BOTTOM_Z = 93.75
LEAD_SCREW_LENGTH = 370.0


def z_lead_screw() -> Part:
    screw = Pos(LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y, LEAD_SCREW_BOTTOM_Z) * Cylinder(
        LEAD_SCREW_DIAMETER / 2, LEAD_SCREW_LENGTH, align=BOTTOM
    )
    screw.label = "z_lead_screw"
    return screw
