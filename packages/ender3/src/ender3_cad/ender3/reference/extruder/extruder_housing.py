from build123d import Box, Cone, Cylinder, Part, Plane, Polyline, Pos, extrude, make_face

from ender3_cad.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_LEFT, FACE_RIGHT
from ender3_cad.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLES
from ender3_cad.ender3.reference.construction import outline_face
from ender3_cad.ender3.reference.dimensions import CUT_THROUGH_LENGTH
from ender3_cad.ender3.reference.extruder.construction import x_cylinder
from ender3_cad.ender3.reference.extruder.dimensions import (
    EXTRUDER_MOUNT_LOCATION,
    FILAMENT_PATH_LOCAL_YZ,
    HOUSING_BASE_THICKNESS,
    HOUSING_FRONT_X,
    MOTOR_HOLE_HALF_SPACING,
    SPRING_BOSS_CHAMFER,
    SPRING_BOSS_DIAMETER,
)

HOUSING_BASE_OUTLINE = [
    (-17.9725, -21.0275),
    (21.0275, -21.0275),
    (21.0275, 20.9725),
    (-17.9725, 20.9725),
    (-20.9725, 17.9725),
    (-20.9725, -18.0275),
]
HOUSING_BASE_CORNER_RADII = [0.0, 5.025, 5.0, 0.0, 0.0, 0.0]
HOUSING_MOTOR_HOLE_DIAMETER = 3.518
HOUSING_COUNTERSINK_DIAMETER = 5.518
HOUSING_COUNTERSINK_DEPTH = 1.0
HOUSING_COUNTERSUNK_HOLE = (-MOTOR_HOLE_HALF_SPACING, MOTOR_HOLE_HALF_SPACING)

HOUSING_GEAR_OPENING_CENTER = (-0.0162, 0.0775)
HOUSING_GEAR_OPENING_DIAMETER = 23.115
HOUSING_BLOCK_BACK_X = 6.455

HOUSING_IDLER_SLOT_X_RANGE = (1.94, HOUSING_BLOCK_BACK_X)
HOUSING_IDLER_SLOT_END_Y = 17.9635
HOUSING_FILAMENT_WINDOW_X_END = 11.115
HOUSING_FILAMENT_WINDOW_Y_RANGE = (-5.1485, 5.3035)
HOUSING_BLOCK_TOP_Z = 15.075
HOUSING_BLOCK_X_RANGE = (HOUSING_BLOCK_BACK_X, 11.279)
HOUSING_BLOCK_PROFILE = [
    (-21.0275, HOUSING_BASE_THICKNESS),
    (20.9725, HOUSING_BASE_THICKNESS),
    (20.9725, 12.075),
    (17.9725, HOUSING_BLOCK_TOP_Z),
    (-16.0025, HOUSING_BLOCK_TOP_Z),
    (-21.0275, 10.05),
]
HOUSING_TONGUE_X_START = 3.7742
HOUSING_TONGUE_Y_RANGE = (-12.1835, 0.0775)
HOUSING_GEAR_CLEARANCE_DIAMETER = 10.653
HOUSING_GEAR_CLEARANCE_CENTERS = [(1.1285, 0.0775), (1.1285, -12.1835)]
HOUSING_NOSE_PROFILE = [
    (-14.5, 0.0),
    (2.5, 0.0),
    (2.5, HOUSING_BASE_THICKNESS),
    (0.0775, HOUSING_BASE_THICKNESS),
    (0.0775, 10.05),
    (-4.9475, HOUSING_BLOCK_TOP_Z),
    (-6.9575, HOUSING_BLOCK_TOP_Z),
    (-11.9825, 10.05),
    (-11.9825, HOUSING_BASE_THICKNESS),
    (-14.5, HOUSING_BASE_THICKNESS),
]
HOUSING_NOSE_CORNER_RADII = [
    0.0,
    0.0,
    0.0,
    1.5075,
    1.5075,
    1.5075,
    1.5075,
    1.5075,
    1.5075,
    0.0,
]
HOUSING_FILAMENT_HOLE_DIAMETER = 2.814
HOUSING_COUPLER_BORE_DIAMETER = 8.3
HOUSING_COUPLER_BORE_X_START = 8.0275
HOUSING_COUPLER_INSERT_X_RANGE = (17.0275, HOUSING_FRONT_X)
HOUSING_COUPLER_INSERT_GROOVE_X_RANGE = (18.2275, 19.9275)
HOUSING_COUPLER_INSERT_GROOVE_DIAMETER = 7.5
HOUSING_COUPLER_INSERT_THREAD_DIAMETER = 5.0
HOUSING_COUPLER_INSERT_CHAMFER = 0.5
HOUSING_SPRING_BOSS_CENTER = (14.851, 9.5475)
HOUSING_SPRING_BOSS_X_RANGE = (3.44, HOUSING_BLOCK_BACK_X)


def extruder_housing() -> Part:
    base = extrude(
        outline_face(HOUSING_BASE_OUTLINE, HOUSING_BASE_CORNER_RADII),
        HOUSING_BASE_THICKNESS,
    )
    base -= Pos(*HOUSING_GEAR_OPENING_CENTER) * Cylinder(HOUSING_GEAR_OPENING_DIAMETER / 2, CUT_THROUGH_LENGTH)
    slot_x_start, slot_x_end = HOUSING_IDLER_SLOT_X_RANGE
    base -= Pos((slot_x_start + slot_x_end) / 2, HOUSING_IDLER_SLOT_END_Y / 2) * Box(
        slot_x_end - slot_x_start, HOUSING_IDLER_SLOT_END_Y, CUT_THROUGH_LENGTH
    )
    window_y_start, window_y_end = HOUSING_FILAMENT_WINDOW_Y_RANGE
    base -= Pos(HOUSING_FILAMENT_WINDOW_X_END / 2, (window_y_start + window_y_end) / 2) * Box(
        HOUSING_FILAMENT_WINDOW_X_END, window_y_end - window_y_start, CUT_THROUGH_LENGTH
    )

    block_x_start, block_x_end = HOUSING_BLOCK_X_RANGE
    block = extrude(
        Plane.YZ.offset(block_x_start) * make_face(Polyline(*HOUSING_BLOCK_PROFILE, close=True)),
        block_x_end - block_x_start,
    )
    tongue_y_start, tongue_y_end = HOUSING_TONGUE_Y_RANGE
    tongue_height = HOUSING_BLOCK_TOP_Z - HOUSING_BASE_THICKNESS
    tongue = Pos(
        (HOUSING_TONGUE_X_START + block_x_start) / 2,
        (tongue_y_start + tongue_y_end) / 2,
        HOUSING_BASE_THICKNESS + tongue_height / 2,
    ) * Box(
        block_x_start - HOUSING_TONGUE_X_START,
        tongue_y_end - tongue_y_start,
        tongue_height,
    )
    tongue -= [
        Pos(x, y) * Cylinder(HOUSING_GEAR_CLEARANCE_DIAMETER / 2, CUT_THROUGH_LENGTH)
        for x, y in HOUSING_GEAR_CLEARANCE_CENTERS
    ]
    nose = extrude(
        Plane.YZ.offset(block_x_end) * outline_face(HOUSING_NOSE_PROFILE, HOUSING_NOSE_CORNER_RADII),
        HOUSING_FRONT_X - block_x_end,
    )
    spring_boss_start, spring_boss_end = HOUSING_SPRING_BOSS_X_RANGE
    spring_boss = x_cylinder(
        SPRING_BOSS_DIAMETER,
        spring_boss_start + SPRING_BOSS_CHAMFER,
        spring_boss_end,
        *HOUSING_SPRING_BOSS_CENTER,
    ) + Pos(spring_boss_start + SPRING_BOSS_CHAMFER / 2, *HOUSING_SPRING_BOSS_CENTER) * FACE_RIGHT * Cone(
        SPRING_BOSS_DIAMETER / 2 - SPRING_BOSS_CHAMFER,
        SPRING_BOSS_DIAMETER / 2,
        SPRING_BOSS_CHAMFER,
    )
    housing = base + block + tongue + nose + spring_boss
    housing -= [
        Pos(x, y) * Cylinder(HOUSING_MOTOR_HOLE_DIAMETER / 2, HOUSING_BASE_THICKNESS, align=BOTTOM)
        for x, y in NEMA17_MOUNTING_HOLES
    ]
    housing -= Pos(
        *HOUSING_COUNTERSUNK_HOLE,
        HOUSING_BASE_THICKNESS - HOUSING_COUNTERSINK_DEPTH / 2,
    ) * Cone(
        HOUSING_MOTOR_HOLE_DIAMETER / 2,
        HOUSING_COUNTERSINK_DIAMETER / 2,
        HOUSING_COUNTERSINK_DEPTH,
    )

    housing -= x_cylinder(
        HOUSING_FILAMENT_HOLE_DIAMETER,
        HOUSING_TONGUE_X_START - CUT_OVERSHOOT,
        HOUSING_COUPLER_BORE_X_START,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    housing -= x_cylinder(
        HOUSING_COUPLER_BORE_DIAMETER,
        HOUSING_COUPLER_BORE_X_START,
        HOUSING_FRONT_X + CUT_OVERSHOOT,
        *FILAMENT_PATH_LOCAL_YZ,
    )

    insert_start, insert_end = HOUSING_COUPLER_INSERT_X_RANGE
    groove_start, groove_end = HOUSING_COUPLER_INSERT_GROOVE_X_RANGE
    insert = x_cylinder(HOUSING_COUPLER_BORE_DIAMETER, insert_start, insert_end, *FILAMENT_PATH_LOCAL_YZ)
    insert -= x_cylinder(
        HOUSING_COUPLER_BORE_DIAMETER + CUT_OVERSHOOT,
        groove_start,
        groove_end,
        *FILAMENT_PATH_LOCAL_YZ,
    ) - x_cylinder(
        HOUSING_COUPLER_INSERT_GROOVE_DIAMETER,
        groove_start,
        groove_end,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    insert -= x_cylinder(
        HOUSING_COUPLER_INSERT_THREAD_DIAMETER,
        insert_start,
        insert_end,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    chamfer_cone = Cone(
        HOUSING_COUPLER_INSERT_THREAD_DIAMETER / 2 + HOUSING_COUPLER_INSERT_CHAMFER,
        HOUSING_COUPLER_INSERT_THREAD_DIAMETER / 2,
        HOUSING_COUPLER_INSERT_CHAMFER,
    )
    insert -= (
        Pos(insert_start + HOUSING_COUPLER_INSERT_CHAMFER / 2, *FILAMENT_PATH_LOCAL_YZ) * FACE_RIGHT * chamfer_cone
    )
    insert -= Pos(insert_end - HOUSING_COUPLER_INSERT_CHAMFER / 2, *FILAMENT_PATH_LOCAL_YZ) * FACE_LEFT * chamfer_cone

    housing = EXTRUDER_MOUNT_LOCATION * (housing + insert)
    housing.label = "extruder_housing"
    return housing
