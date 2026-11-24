from math import radians, tan

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Cylinder,
    Part,
    Plane,
    Polygon,
    Pos,
    Rectangle,
    RectangleRounded,
    chamfer,
    extrude,
    fillet,
    mirror,
)

from ender3_cad.dimensions import BOTTOM, TOP

CR_TOUCH_TAB_LENGTH = 27.2
CR_TOUCH_TAB_WIDTH = 9.5
CR_TOUCH_TAB_CENTER_Y = -1.0
CR_TOUCH_TAB_THICKNESS = 1.9
CR_TOUCH_TAB_CORNER_RADIUS = 0.5
CR_TOUCH_MOUNT_HOLE_SPACING = 18.0
CR_TOUCH_MOUNT_HOLE_Y = -2.25
CR_TOUCH_MOUNT_HOLE_DIAMETER = 3.2
CR_TOUCH_MOUNT_HOLES = [
    (-CR_TOUCH_MOUNT_HOLE_SPACING / 2, CR_TOUCH_MOUNT_HOLE_Y),
    (CR_TOUCH_MOUNT_HOLE_SPACING / 2, CR_TOUCH_MOUNT_HOLE_Y),
]
CR_TOUCH_BODY_WIDTH = 16.2
CR_TOUCH_BODY_DEPTH = 17.5
CR_TOUCH_BODY_CORNER_RADIUS = 4.0
CR_TOUCH_BODY_SIDE_DRAFT_ANGLE = 1.0
CR_TOUCH_MOUNT_TO_BODY_BOTTOM = 37.0
CR_TOUCH_MOUNT_TO_TAPER_START = 30.0
CR_TOUCH_BODY_BOTTOM_DEPTH = 14.2
CR_TOUCH_SIDE_PANEL_RECESS = 0.75
CR_TOUCH_SIDE_PANEL_SPAN = (6.5, 28.5)
CR_TOUCH_SIDE_PANEL_RAMP_ANGLE = 60.0
CR_TOUCH_SCREW_POCKET_INNER_X = 6.3
CR_TOUCH_SCREW_POCKET_Y = (-5.2, 0.7)
CR_TOUCH_SCREW_POCKET_DEPTH = 10.0
CR_TOUCH_GUSSET_Y = (0.7, 1.9)
CR_TOUCH_GUSSET_DEPTH = 5.0
CR_TOUCH_GUSSET_FILLET_RADIUS = 3.0
CR_TOUCH_GUSSET_EDGE_ROUND = 0.5
CR_TOUCH_PIN_HOUSING_DIAMETER = 5.8
CR_TOUCH_PIN_HOUSING_DEPTH = 2.0
CR_TOUCH_PIN_STEM_DIAMETER = 1.9
CR_TOUCH_PIN_COLLAR_DIAMETER = 3.2
CR_TOUCH_PIN_COLLAR_SPAN = (36.0, 37.5)
CR_TOUCH_PIN_DIAMETER = 2.4
CR_TOUCH_PIN_TIP_CHAMFER = 0.7
CR_TOUCH_MOUNT_TO_PIN_TIP = 39.4


def cr_touch() -> Part:
    draft = tan(radians(CR_TOUCH_BODY_SIDE_DRAFT_ANGLE))
    corner_half_width = CR_TOUCH_BODY_WIDTH / 2 - CR_TOUCH_BODY_DEPTH / 2 * draft
    plan = Polygon(
        (CR_TOUCH_BODY_WIDTH / 2, 0),
        (corner_half_width, CR_TOUCH_BODY_DEPTH / 2),
        (-corner_half_width, CR_TOUCH_BODY_DEPTH / 2),
        (-CR_TOUCH_BODY_WIDTH / 2, 0),
        (-corner_half_width, -CR_TOUCH_BODY_DEPTH / 2),
        (corner_half_width, -CR_TOUCH_BODY_DEPTH / 2),
    )
    plan = fillet(
        plan.vertices().group_by(Axis.Y)[0] + plan.vertices().group_by(Axis.Y)[-1], CR_TOUCH_BODY_CORNER_RADIUS
    )

    panel_top, panel_bottom = CR_TOUCH_SIDE_PANEL_SPAN
    ramp_height = CR_TOUCH_SIDE_PANEL_RECESS * tan(radians(CR_TOUCH_SIDE_PANEL_RAMP_ANGLE))
    panel_y = CR_TOUCH_BODY_DEPTH / 2 - CR_TOUCH_SIDE_PANEL_RECESS
    half_side = [
        (CR_TOUCH_BODY_DEPTH / 2, 0),
        (CR_TOUCH_BODY_DEPTH / 2, ramp_height - panel_top),
        (panel_y, -panel_top),
        (panel_y, -panel_bottom),
        (CR_TOUCH_BODY_DEPTH / 2, -panel_bottom - ramp_height),
        (CR_TOUCH_BODY_DEPTH / 2, -CR_TOUCH_MOUNT_TO_TAPER_START),
        (CR_TOUCH_BODY_BOTTOM_DEPTH / 2, -CR_TOUCH_MOUNT_TO_BODY_BOTTOM),
    ]
    side = Polygon(*half_side, *[(-y, z) for y, z in reversed(half_side)])

    body = Pos(0, 0, -CR_TOUCH_MOUNT_TO_BODY_BOTTOM) * extrude(plan, CR_TOUCH_MOUNT_TO_BODY_BOTTOM)
    body &= extrude(Plane.YZ * side, CR_TOUCH_BODY_WIDTH / 2, both=True)
    screw_pocket = Pos(CR_TOUCH_SCREW_POCKET_INNER_X, CR_TOUCH_SCREW_POCKET_Y[0], 0) * Box(
        CR_TOUCH_TAB_LENGTH / 2 - CR_TOUCH_SCREW_POCKET_INNER_X,
        CR_TOUCH_SCREW_POCKET_Y[1] - CR_TOUCH_SCREW_POCKET_Y[0],
        CR_TOUCH_SCREW_POCKET_DEPTH,
        align=(Align.MIN, Align.MIN, Align.MAX),
    )
    body -= screw_pocket + mirror(screw_pocket, Plane.YZ)
    body -= Pos(0, 0, -CR_TOUCH_MOUNT_TO_BODY_BOTTOM) * Cylinder(
        CR_TOUCH_PIN_HOUSING_DIAMETER / 2, CR_TOUCH_PIN_HOUSING_DEPTH, align=BOTTOM
    )

    tabs = Pos(0, CR_TOUCH_TAB_CENTER_Y, -CR_TOUCH_TAB_THICKNESS) * extrude(
        RectangleRounded(CR_TOUCH_TAB_LENGTH, CR_TOUCH_TAB_WIDTH, CR_TOUCH_TAB_CORNER_RADIUS), CR_TOUCH_TAB_THICKNESS
    )
    for x, y in CR_TOUCH_MOUNT_HOLES:
        tabs -= Pos(x, y, -CR_TOUCH_TAB_THICKNESS) * Cylinder(
            CR_TOUCH_MOUNT_HOLE_DIAMETER / 2, CR_TOUCH_TAB_THICKNESS, align=BOTTOM
        )

    fillet_x = CR_TOUCH_BODY_WIDTH / 2 + CR_TOUCH_GUSSET_FILLET_RADIUS
    fillet_z = -CR_TOUCH_GUSSET_DEPTH - CR_TOUCH_GUSSET_FILLET_RADIUS
    gusset_profile = RectangleRounded(
        CR_TOUCH_TAB_LENGTH, CR_TOUCH_GUSSET_DEPTH, CR_TOUCH_GUSSET_EDGE_ROUND, align=(Align.CENTER, Align.MAX)
    ) + Pos(0, -CR_TOUCH_GUSSET_DEPTH) * Rectangle(
        2 * fillet_x, CR_TOUCH_GUSSET_FILLET_RADIUS, align=(Align.CENTER, Align.MAX)
    )
    for x in (-fillet_x, fillet_x):
        gusset_profile -= Pos(x, fillet_z) * Circle(CR_TOUCH_GUSSET_FILLET_RADIUS)
    gussets = Pos(0, CR_TOUCH_GUSSET_Y[1], 0) * extrude(
        Plane.XZ * gusset_profile, CR_TOUCH_GUSSET_Y[1] - CR_TOUCH_GUSSET_Y[0]
    )

    pin_housing_ceiling = CR_TOUCH_MOUNT_TO_BODY_BOTTOM - CR_TOUCH_PIN_HOUSING_DEPTH
    pin = Pos(0, 0, -pin_housing_ceiling) * Cylinder(
        CR_TOUCH_PIN_STEM_DIAMETER / 2, CR_TOUCH_PIN_COLLAR_SPAN[0] - pin_housing_ceiling, align=TOP
    )
    pin += Pos(0, 0, -CR_TOUCH_PIN_COLLAR_SPAN[0]) * Cylinder(
        CR_TOUCH_PIN_COLLAR_DIAMETER / 2, CR_TOUCH_PIN_COLLAR_SPAN[1] - CR_TOUCH_PIN_COLLAR_SPAN[0], align=TOP
    )
    pin_tip = Pos(0, 0, -CR_TOUCH_PIN_COLLAR_SPAN[1]) * Cylinder(
        CR_TOUCH_PIN_DIAMETER / 2, CR_TOUCH_MOUNT_TO_PIN_TIP - CR_TOUCH_PIN_COLLAR_SPAN[1], align=TOP
    )
    pin += chamfer(pin_tip.edges().group_by(Axis.Z)[0], CR_TOUCH_PIN_TIP_CHAMFER)

    probe = body + tabs + gussets + pin
    probe.label = "cr_touch"
    return probe
