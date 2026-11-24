from build123d import Axis, Cylinder, Part, Plane, Polygon, Pos, Rot, revolve

from ender3_cad.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_RIGHT
from ender3_cad.ender3.reference.components.dimensions import GT2_PULLEY_BORE_RADIUS, GT2_PULLEY_FLANGE_RADIUS
from ender3_cad.ender3.reference.components.gt2_pulley_friction_fit import gt2_pulley_friction_fit

GT2_PULLEY_HUB_LENGTH = 7.0
GT2_PULLEY_HUB_END_CHAMFER = 0.5
GT2_PULLEY_SET_SCREW_DIAMETER = 2.0
GT2_PULLEY_SET_SCREW_HEIGHT = 5.035621
GT2_PULLEY_SET_SCREW_ANGLES = (0.0, 60.0)


def gt2_pulley() -> Part:
    chamfer = GT2_PULLEY_HUB_END_CHAMFER
    hub_profile = [
        (GT2_PULLEY_BORE_RADIUS, 0),
        (GT2_PULLEY_FLANGE_RADIUS - chamfer, 0),
        (GT2_PULLEY_FLANGE_RADIUS, chamfer),
        (GT2_PULLEY_FLANGE_RADIUS, GT2_PULLEY_HUB_LENGTH),
        (GT2_PULLEY_BORE_RADIUS, GT2_PULLEY_HUB_LENGTH),
    ]
    pulley = (
        revolve(Plane.XZ * Polygon(*hub_profile, align=None), Axis.Z)
        + Pos(0, 0, GT2_PULLEY_HUB_LENGTH) * gt2_pulley_friction_fit()
    )
    for angle in GT2_PULLEY_SET_SCREW_ANGLES:
        pulley -= (
            Rot(0, 0, angle)
            * Pos(0, 0, GT2_PULLEY_SET_SCREW_HEIGHT)
            * FACE_RIGHT
            * Cylinder(GT2_PULLEY_SET_SCREW_DIAMETER / 2, GT2_PULLEY_FLANGE_RADIUS + CUT_OVERSHOOT, align=BOTTOM)
        )
    pulley.label = "gt2_pulley"
    return pulley
