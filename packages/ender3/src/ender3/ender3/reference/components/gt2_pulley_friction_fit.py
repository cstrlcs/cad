from build123d import Axis, Circle, Part, Plane, Polygon, Pos, Rot, extrude, revolve

from ender3.ender3.reference.components.dimensions import GT2_PULLEY_BORE_RADIUS, GT2_PULLEY_FLANGE_RADIUS

GT2_PULLEY_FLANGE_THICKNESS = 0.5
GT2_PULLEY_INNER_FLANGE_CHAMFER = 0.5
GT2_PULLEY_TOOTH_TIP_RADIUS = 6.0
GT2_PULLEY_TOOTH_LENGTH = 8.0
GT2_PULLEY_GROOVE_COUNT = 15
GT2_PULLEY_GROOVE_DIAMETER = 1.254342
GT2_PULLEY_GROOVE_PHASE = 16.66

GT2_PULLEY_COUNTERBORE_RADIUS = 4.0
GT2_PULLEY_COUNTERBORE_DEPTH = 0.5


def gt2_pulley_friction_fit() -> Part:
    flange, chamfer = GT2_PULLEY_FLANGE_RADIUS, GT2_PULLEY_INNER_FLANGE_CHAMFER
    tooth_start = GT2_PULLEY_FLANGE_THICKNESS
    tooth_end = tooth_start + GT2_PULLEY_TOOTH_LENGTH
    length = tooth_end + GT2_PULLEY_FLANGE_THICKNESS
    inner_flange = [
        (GT2_PULLEY_BORE_RADIUS, 0),
        (flange, 0),
        (flange - chamfer, tooth_start),
        (GT2_PULLEY_BORE_RADIUS, tooth_start),
    ]
    outer_flange = [
        (GT2_PULLEY_BORE_RADIUS, tooth_end),
        (flange, tooth_end),
        (flange, length),
        (GT2_PULLEY_COUNTERBORE_RADIUS, length),
        (GT2_PULLEY_COUNTERBORE_RADIUS, length - GT2_PULLEY_COUNTERBORE_DEPTH),
        (GT2_PULLEY_BORE_RADIUS, length - GT2_PULLEY_COUNTERBORE_DEPTH),
    ]
    tooth_section = (
        Circle(GT2_PULLEY_TOOTH_TIP_RADIUS)
        - [
            Rot(0, 0, GT2_PULLEY_GROOVE_PHASE + index * 360 / GT2_PULLEY_GROOVE_COUNT)
            * Pos(GT2_PULLEY_TOOTH_TIP_RADIUS, 0)
            * Circle(GT2_PULLEY_GROOVE_DIAMETER / 2)
            for index in range(GT2_PULLEY_GROOVE_COUNT)
        ]
        - Circle(GT2_PULLEY_BORE_RADIUS)
    )
    pulley = (
        revolve(Plane.XZ * Polygon(*inner_flange, align=None), Axis.Z)
        + Pos(0, 0, tooth_start) * extrude(tooth_section, GT2_PULLEY_TOOTH_LENGTH)
        + revolve(Plane.XZ * Polygon(*outer_flange, align=None), Axis.Z)
    )
    pulley.label = "gt2_pulley_friction_fit"
    return pulley
