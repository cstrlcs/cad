from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Part,
    Plane,
    Pos,
    Rectangle,
    SlotCenterToCenter,
    extrude,
    fillet,
    mirror,
)

from ender3.ender3.reference.construction import range_rectangle
from ender3.ender3.reference.y_axis.dimensions import (
    SHEET_BEND_INNER_RADIUS,
    SHEET_BEND_OUTER_RADIUS,
    SHEET_THICKNESS,
    Y_BELT_TENSIONER_HALF_INNER_WIDTH,
    Y_BELT_TENSIONER_SLOT_CENTERS,
    Y_BELT_TENSIONER_SLOT_WIDTH,
    Y_PROFILE_FRONT_END,
)

Y_BELT_TENSIONER_HEIGHT = 40.0
Y_BELT_TENSIONER_FRONT_FACE_Y = -25.0
Y_BELT_TENSIONER_ARM_END_CENTER = (19.0, -10.0)
Y_BELT_TENSIONER_ARM_END_RADIUS = 10.0
Y_BELT_TENSIONER_IDLER_POST_REAR_Y = -5.0
Y_BELT_TENSIONER_IDLER_POST_CORNER_RADIUS = 5.0

Y_BELT_TENSIONER_IDLER_HOLE_CENTER = (-11.0, 15.0)
Y_BELT_TENSIONER_IDLER_HOLE_DIAMETER = 4.2
Y_BELT_TENSIONER_LOCATION = Pos(*Y_PROFILE_FRONT_END)


def y_belt_tensioner() -> Part:
    half_height = Y_BELT_TENSIONER_HEIGHT / 2
    bend_center_x = Y_BELT_TENSIONER_HALF_INNER_WIDTH - SHEET_BEND_INNER_RADIUS
    bend_center_y = Y_BELT_TENSIONER_FRONT_FACE_Y + SHEET_BEND_OUTER_RADIUS
    front_wall = Pos(0, Y_BELT_TENSIONER_FRONT_FACE_Y, -half_height) * Box(
        2 * bend_center_x, SHEET_THICKNESS, Y_BELT_TENSIONER_HEIGHT, align=(Align.CENTER, Align.MIN, Align.MIN)
    )
    bend_section = (Circle(SHEET_BEND_OUTER_RADIUS) - Circle(SHEET_BEND_INNER_RADIUS)) & Rectangle(
        SHEET_BEND_OUTER_RADIUS, SHEET_BEND_OUTER_RADIUS, align=(Align.MIN, Align.MAX)
    )
    bend = Pos(bend_center_x, bend_center_y, -half_height) * extrude(bend_section, Y_BELT_TENSIONER_HEIGHT)
    arm_end_y, arm_end_z = Y_BELT_TENSIONER_ARM_END_CENTER
    arm = range_rectangle((bend_center_y, arm_end_y), (-half_height, 0)) + Pos(arm_end_y, arm_end_z) * Circle(
        Y_BELT_TENSIONER_ARM_END_RADIUS
    )
    idler_post = range_rectangle((bend_center_y, Y_BELT_TENSIONER_IDLER_POST_REAR_Y), (0, half_height))
    side_outline = arm + idler_post
    idler_post_rear_corners = side_outline.vertices().group_by(Axis.X)[1]
    side_outline = fillet(idler_post_rear_corners, Y_BELT_TENSIONER_IDLER_POST_CORNER_RADIUS)
    (slot_start_y, slot_z), (slot_end_y, _) = Y_BELT_TENSIONER_SLOT_CENTERS
    side_outline = (
        side_outline
        - Pos((slot_start_y + slot_end_y) / 2, slot_z)
        * SlotCenterToCenter(slot_end_y - slot_start_y, Y_BELT_TENSIONER_SLOT_WIDTH)
        - Pos(*Y_BELT_TENSIONER_IDLER_HOLE_CENTER) * Circle(Y_BELT_TENSIONER_IDLER_HOLE_DIAMETER / 2)
    )
    side_wall = extrude(Plane.YZ.offset(Y_BELT_TENSIONER_HALF_INNER_WIDTH) * side_outline, SHEET_THICKNESS)
    right_half = bend + side_wall
    tensioner = Y_BELT_TENSIONER_LOCATION * (front_wall + right_half + mirror(right_half, Plane.YZ))
    tensioner.label = "y_belt_tensioner"
    return tensioner
