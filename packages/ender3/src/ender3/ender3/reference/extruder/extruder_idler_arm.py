from build123d import Box, Cone, Cylinder, Location, Part, Pos, Torus, extrude

from ender3.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_DOWN, FACE_LEFT, FACE_RIGHT
from ender3.ender3.reference.construction import outline_face
from ender3.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3.ender3.reference.extruder.construction import x_cylinder
from ender3.ender3.reference.extruder.dimensions import (
    EXTRUDER_MOUNT_LOCATION,
    HOUSING_BASE_THICKNESS,
    MOTOR_HOLE_HALF_SPACING,
    SPRING_BOSS_CHAMFER,
    SPRING_BOSS_DIAMETER,
)

IDLER_PIVOT_HOLE = (-MOTOR_HOLE_HALF_SPACING, -MOTOR_HOLE_HALF_SPACING)

IDLER_PIVOT_HEIGHT = HOUSING_BASE_THICKNESS
IDLER_ANGLE = -4.61487
IDLER_LOCATION = EXTRUDER_MOUNT_LOCATION * Location((*IDLER_PIVOT_HOLE, IDLER_PIVOT_HEIGHT), (0, 0, IDLER_ANGLE))
IDLER_THICKNESS = 10.5525
IDLER_ARM_OUTLINE = [
    (-5.5878, -5.7721),
    (-0.0492, -5.7501),
    (7.2862, -5.3054),
    (7.2862, 3.5479),
    (8.4551, 3.5479),
    (8.4551, 11.3867),
    (3.4572, 16.7534),
    (3.4572, 26.9112),
    (4.4622, 27.4915),
    (4.4622, 45.2109),
    (-3.5938, 45.2109),
    (-3.5938, 35.6888),
    (-5.5878, 28.735),
]
IDLER_ARM_CORNER_RADII = [
    5.025,
    0.0,
    2.01,
    0.0,
    0.0,
    0.0,
    2.01,
    1.005,
    1.005,
    0.0,
    0.0,
    5.0,
    5.0,
]
IDLER_BEARING_PLATE_THICKNESS = 2.9
IDLER_BEARING_PLATE_OUTLINE = [
    (0.0, -5.7471),
    (21.3055, -4.4555),
    (21.3055, 6.975),
    (8.4551, 11.3867),
    (0.0, 11.3867),
]
IDLER_BEARING_PLATE_CORNER_RADII = [0.0, 5.9314, 5.9295, 0.0, 0.0]
IDLER_LEVER_TIP_Y = 45.2109
IDLER_LEVER_X_RANGE = (-3.5938, 4.4622)
IDLER_BEARING_AXIS = (14.5725, 3.5479)
IDLER_BEARING_POCKET_DIAMETER = 14.5725
IDLER_AXLE_BUSHING_DIAMETER = 6.2
IDLER_AXLE_BUSHING_HEIGHT = 3.0
IDLER_AXLE_HOLE_DIAMETER = 3.3
IDLER_AXLE_HOLE_CHAMFER = 0.35
IDLER_PIVOT_HOLE_DIAMETER = 3.216
IDLER_PIVOT_COUNTERBORE_DIAMETER = 6.03
IDLER_PIVOT_COUNTERBORE_FLOOR_Z = 8.04
IDLER_FILAMENT_CHANNEL_DIAMETER = 2.513
IDLER_FILAMENT_CHANNEL_CENTER = (9.447, 5.025)
IDLER_FILAMENT_FUNNEL_RADIUS = 2.5125
IDLER_FILAMENT_CHANNEL_X_RANGE = (-5.5878, 8.4551)
IDLER_SPRING_BOSS_CENTER = (30.3623, 5.5275)
IDLER_SPRING_BOSS_X_RANGE = (4.4622, 7.4772)


def extruder_idler_arm() -> Part:
    arm = extrude(outline_face(IDLER_ARM_OUTLINE, IDLER_ARM_CORNER_RADII), IDLER_THICKNESS)
    arm -= Pos(*IDLER_BEARING_AXIS, IDLER_BEARING_PLATE_THICKNESS) * Cylinder(
        IDLER_BEARING_POCKET_DIAMETER / 2, IDLER_THICKNESS, align=BOTTOM
    )
    arm += extrude(
        outline_face(IDLER_BEARING_PLATE_OUTLINE, IDLER_BEARING_PLATE_CORNER_RADII),
        IDLER_BEARING_PLATE_THICKNESS,
    )
    lever_x_start, lever_x_end = IDLER_LEVER_X_RANGE
    lever_tip_radius = IDLER_THICKNESS / 2
    arm += x_cylinder(IDLER_THICKNESS, lever_x_start, lever_x_end, IDLER_LEVER_TIP_Y, lever_tip_radius) & Pos(
        0, IDLER_LEVER_TIP_Y + lever_tip_radius
    ) * Box(CUT_THROUGH_LENGTH, 2 * lever_tip_radius, CUT_THROUGH_LENGTH)
    arm += Pos(*IDLER_BEARING_AXIS) * Cylinder(IDLER_AXLE_BUSHING_DIAMETER / 2, IDLER_AXLE_BUSHING_HEIGHT, align=BOTTOM)
    spring_boss_start, spring_boss_end = IDLER_SPRING_BOSS_X_RANGE
    arm += x_cylinder(
        SPRING_BOSS_DIAMETER,
        spring_boss_start,
        spring_boss_end - SPRING_BOSS_CHAMFER,
        *IDLER_SPRING_BOSS_CENTER,
    ) + Pos(spring_boss_end - SPRING_BOSS_CHAMFER / 2, *IDLER_SPRING_BOSS_CENTER) * FACE_LEFT * Cone(
        SPRING_BOSS_DIAMETER / 2 - SPRING_BOSS_CHAMFER,
        SPRING_BOSS_DIAMETER / 2,
        SPRING_BOSS_CHAMFER,
    )

    arm -= Cylinder(IDLER_PIVOT_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH)
    arm -= Pos(0, 0, IDLER_PIVOT_COUNTERBORE_FLOOR_Z) * Cylinder(
        IDLER_PIVOT_COUNTERBORE_DIAMETER / 2, IDLER_THICKNESS, align=BOTTOM
    )
    arm -= Pos(*IDLER_BEARING_AXIS) * Cylinder(IDLER_AXLE_HOLE_DIAMETER / 2, CUT_THROUGH_LENGTH)
    axle_chamfer = Cone(
        IDLER_AXLE_HOLE_DIAMETER / 2 + IDLER_AXLE_HOLE_CHAMFER,
        IDLER_AXLE_HOLE_DIAMETER / 2,
        IDLER_AXLE_HOLE_CHAMFER,
    )
    arm -= Pos(*IDLER_BEARING_AXIS, IDLER_AXLE_HOLE_CHAMFER / 2) * axle_chamfer
    arm -= Pos(*IDLER_BEARING_AXIS, IDLER_AXLE_BUSHING_HEIGHT - IDLER_AXLE_HOLE_CHAMFER / 2) * FACE_DOWN * axle_chamfer

    channel_start, channel_end = IDLER_FILAMENT_CHANNEL_X_RANGE
    funnel_end_x = channel_start + IDLER_FILAMENT_FUNNEL_RADIUS
    funnel_mouth_radius = IDLER_FILAMENT_CHANNEL_DIAMETER / 2 + IDLER_FILAMENT_FUNNEL_RADIUS
    arm -= x_cylinder(
        IDLER_FILAMENT_CHANNEL_DIAMETER,
        channel_start - CUT_OVERSHOOT,
        channel_end + CUT_OVERSHOOT,
        *IDLER_FILAMENT_CHANNEL_CENTER,
    )
    arm -= x_cylinder(
        2 * funnel_mouth_radius,
        channel_start - CUT_OVERSHOOT,
        funnel_end_x,
        *IDLER_FILAMENT_CHANNEL_CENTER,
    ) - Pos(funnel_end_x, *IDLER_FILAMENT_CHANNEL_CENTER) * FACE_RIGHT * Torus(
        funnel_mouth_radius, IDLER_FILAMENT_FUNNEL_RADIUS
    )

    arm = IDLER_LOCATION * arm
    arm.label = "extruder_idler_arm"
    return arm
