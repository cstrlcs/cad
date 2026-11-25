from build123d import (
    Cone,
    Cylinder,
    FilletPolyline,
    Part,
    Plane,
    Polygon,
    Pos,
    RectangleRounded,
    SlotOverall,
    Transition,
    Vector,
    Wire,
    extrude,
    loft,
    mirror,
    sweep,
)

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block
from ender3.dimensions import BOTTOM, CUT_OVERSHOOT, M2_PILOT_DIAMETER, M3_PILOT_DIAMETER
from ender3.ender3.purchased.blower_5015 import (
    BLOWER_5015_LATCH_Y,
    BLOWER_5015_LATCH_Z,
    BLOWER_5015_OUTLET_OPENING_HEIGHT,
    BLOWER_5015_OUTLET_OPENING_WIDTH,
    BLOWER_5015_OUTLET_WIDTH,
    BLOWER_5015_THICKNESS,
)
from ender3.ender3.reference.components.dimensions import (
    FAN_4010_BORE_DIAMETER,
    FAN_4010_MOUNTING_HOLES,
    FAN_4010_SIZE,
)
from ender3.ender3.reference.print_head.dimensions import (
    HOTEND_AXIS_X,
    HOTEND_AXIS_Y,
    X_CARRIAGE_PLATE_CENTER_HOLE_POINT,
    X_CARRIAGE_PLATE_HOTEND_STANDOFF_HEIGHT,
    X_CARRIAGE_PLATE_HOTEND_STANDOFFS,
    X_CARRIAGE_PLATE_LOCATION,
    X_CARRIAGE_PLATE_UPPER_HOLE_POINTS,
)
from ender3.upgrades.fan_duct.dimensions import (
    ARM_SIDE_X_OFFSET,
    ARM_SIZE,
    BLOWER_FACE_DOWN,
    FLANGE_PLANE,
    MEASURED_NOZZLE_TIP_Z,
    SOCKET_CENTER_DOWN,
    SOCKET_DEPTH,
)

CUTTER_OVERLAP = 0.05

CARRIAGE_PLATE_FRONT_Y = X_CARRIAGE_PLATE_LOCATION.position.Y
STANDOFF_POINTS = [
    (X_CARRIAGE_PLATE_LOCATION.position.X + x, X_CARRIAGE_PLATE_LOCATION.position.Z + z)
    for x, z in X_CARRIAGE_PLATE_HOTEND_STANDOFFS
]
WHEEL_NUT_POINTS = [
    (point[0], point[2]) for point in [X_CARRIAGE_PLATE_CENTER_HOLE_POINT, *X_CARRIAGE_PLATE_UPPER_HOLE_POINTS]
]
WHEEL_NUT_CLEARANCE_DIAMETER = 13.0
WHEEL_NUT_CLEARANCE_DEPTH = 9.0

DUCT_WALL = 1.35
CAGE_WALL = 1.8
CAGE_SIDE_WALL = 2.6
FLANGE_THICKNESS = 2.0

STANDOFF_CLAMP_GAP = 0.15
STANDOFF_PLATE_THICKNESS = X_CARRIAGE_PLATE_HOTEND_STANDOFF_HEIGHT - STANDOFF_CLAMP_GAP
STANDOFF_PLATE_FRONT_Y = CARRIAGE_PLATE_FRONT_Y - STANDOFF_PLATE_THICKNESS
STANDOFF_CLEARANCE_DIAMETER = 5.9
CAGE_OUTER_HALF_WIDTH = 14.0
CAGE_INNER_HALF_WIDTH = CAGE_OUTER_HALF_WIDTH - CAGE_SIDE_WALL
CAGE_FRONT_DISTANCE_FROM_HOTEND_AXIS = 8.3
CAGE_FRONT_Y = HOTEND_AXIS_Y - CAGE_FRONT_DISTANCE_FROM_HOTEND_AXIS
CAGE_Z_RANGE = (257.05, 282.45)
STANDOFF_PLATE_Z_RANGE = (266.0, CAGE_Z_RANGE[1])
STANDOFF_PLATE_GAP_HALF_WIDTH = 2.4
EXHAUST_SLOT_SOLID_ROOT_LENGTH = 5.0
EXHAUST_SLOT_FRONT_INSET = 1.25
EXHAUST_SLOT_Y = (CAGE_FRONT_Y + EXHAUST_SLOT_FRONT_INSET, STANDOFF_PLATE_FRONT_Y - EXHAUST_SLOT_SOLID_ROOT_LENGTH)
EXHAUST_SLOT_Z_RANGES = [(261.25, 264.75), (268.75, 272.25)]

FLANGE_CORNER_RADIUS = 3.0
FUNNEL_REAR_Z_RANGE = (252.5, 285.0)
FUNNEL_REAR_CORNER_RADIUS = 3.0
FUNNEL_REAR_INNER_CORNER_RADIUS = 2.0
FAN_BORE_LIP = 0.5
FUNNEL_FRONT_SIZE = FAN_4010_BORE_DIAMETER - 2 * FAN_BORE_LIP
FUNNEL_FRONT_CORNER_RADIUS = 15.0
FAN_SCREW_BOSS_DIAMETER = 7.0
FAN_SCREW_BOSS_DEPTH = 5.0

SOCKET_FIT_CLEARANCE = 0.3

SOCKET_INNER = (
    BLOWER_5015_OUTLET_WIDTH + 2 * SOCKET_FIT_CLEARANCE,
    BLOWER_5015_THICKNESS + 2 * SOCKET_FIT_CLEARANCE,
)
SOCKET_OUTER = (SOCKET_INNER[0] + 2 * CAGE_WALL, SOCKET_INNER[1] + 2 * CAGE_WALL)
PASSAGE_CLEARANCE = 0.4
PASSAGE = (BLOWER_5015_OUTLET_OPENING_WIDTH + PASSAGE_CLEARANCE, BLOWER_5015_OUTLET_OPENING_HEIGHT + PASSAGE_CLEARANCE)
PLENUM_DEPTH = 10.0
LATCH_WINDOW_CLEARANCE = 0.5
VOLUTE_RELIEF_REMAINING_WALL = 2.0
VOLUTE_RELIEF_DEPTH = SOCKET_DEPTH - VOLUTE_RELIEF_REMAINING_WALL
CLAMP_SCREW_X_OFFSETS = (-9.0, 9.0)
CLAMP_SCREW_DEPTH = 3.0
CLAMP_SCREW_BOSS_DIAMETER = 5.0
CLAMP_SCREW_BOSS_HEIGHT = 2.5

ARM_CORNER_RADIUS = 3.0
ARM_CENTER_Z = 240.0
ARM_FRONT_Y = -94.5
ARM_TURN_RADIUS = 12.0

OUTLET_INNER_X_OFFSET = 16.5
OUTLET_EXIT_Z = 233.95
OUTLET_AIM_BELOW_NOZZLE_TIP = 1.3
OUTLET_GAP = 4.0
OUTLET_ENTRY_GAP = 5.0
OUTLET_LENGTH = 12.0
OUTLET_Y_RANGE = (-71.55, -56.85)
OUTLET_EXIT_CENTER = Vector(HOTEND_AXIS_X + OUTLET_INNER_X_OFFSET, sum(OUTLET_Y_RANGE) / 2, OUTLET_EXIT_Z)
OUTLET_DIRECTION = (
    Vector(HOTEND_AXIS_X, OUTLET_EXIT_CENTER.Y, MEASURED_NOZZLE_TIP_Z - OUTLET_AIM_BELOW_NOZZLE_TIP)
    - OUTLET_EXIT_CENTER
).normalized()
ARM_END_Y = OUTLET_Y_RANGE[1]
NUT_STEP_CLEARANCE = 0.5
NUT_STEP_FRONT_Y = CARRIAGE_PLATE_FRONT_Y - WHEEL_NUT_CLEARANCE_DEPTH - NUT_STEP_CLEARANCE
NUT_STEP_TOP_Z = WHEEL_NUT_POINTS[0][1] - WHEEL_NUT_CLEARANCE_DIAMETER / 2 - NUT_STEP_CLEARANCE


def _cylinder(start: Vector, direction: Vector, diameter: float, length: float) -> Part:
    return Plane(origin=tuple(start), z_dir=tuple(direction)).location * Cylinder(diameter / 2, length, align=BOTTOM)


def _flange_box(
    x_range: tuple[float, float], down_range: tuple[float, float], depth_range: tuple[float, float]
) -> Part:
    return FLANGE_PLANE.location * block(x_range, down_range, depth_range)


def _wheel_nut_clearance() -> Part:
    return Part() + [
        _cylinder(
            Vector(x, CARRIAGE_PLATE_FRONT_Y, z),
            Vector(0, -1, 0),
            WHEEL_NUT_CLEARANCE_DIAMETER,
            WHEEL_NUT_CLEARANCE_DEPTH,
        )
        for x, z in WHEEL_NUT_POINTS
    ]


def _cage() -> Part:
    outer_x = (HOTEND_AXIS_X - CAGE_OUTER_HALF_WIDTH, HOTEND_AXIS_X + CAGE_OUTER_HALF_WIDTH)
    walls = [
        block(x_range, (CAGE_FRONT_Y, CARRIAGE_PLATE_FRONT_Y), CAGE_Z_RANGE)
        for x_range in [
            (outer_x[0], outer_x[0] + CAGE_SIDE_WALL),
            (outer_x[1] - CAGE_SIDE_WALL, outer_x[1]),
        ]
    ]
    exhaust_slots = [
        extrude(
            Plane(origin=(HOTEND_AXIS_X, sum(EXHAUST_SLOT_Y) / 2, sum(z_range) / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
            * SlotOverall(EXHAUST_SLOT_Y[1] - EXHAUST_SLOT_Y[0], z_range[1] - z_range[0]),
            CAGE_OUTER_HALF_WIDTH + CUT_OVERSHOOT,
            both=True,
        )
        for z_range in EXHAUST_SLOT_Z_RANGES
    ]
    plate = block(outer_x, (STANDOFF_PLATE_FRONT_Y, CARRIAGE_PLATE_FRONT_Y), STANDOFF_PLATE_Z_RANGE) - block(
        (HOTEND_AXIS_X - STANDOFF_PLATE_GAP_HALF_WIDTH, HOTEND_AXIS_X + STANDOFF_PLATE_GAP_HALF_WIDTH),
        (STANDOFF_PLATE_FRONT_Y, CARRIAGE_PLATE_FRONT_Y),
        STANDOFF_PLATE_Z_RANGE,
    )
    standoff_holes = [
        _cylinder(
            Vector(x, CARRIAGE_PLATE_FRONT_Y, z),
            Vector(0, -1, 0),
            STANDOFF_CLEARANCE_DIAMETER,
            STANDOFF_PLATE_THICKNESS,
        )
        for x, z in STANDOFF_POINTS
    ]
    return Part() + walls - exhaust_slots + plate - standoff_holes


def _funnel() -> Part:
    rear_center_z = sum(FUNNEL_REAR_Z_RANGE) / 2
    rear_height = FUNNEL_REAR_Z_RANGE[1] - FUNNEL_REAR_Z_RANGE[0]
    rear_plane = Plane(origin=(HOTEND_AXIS_X, CAGE_FRONT_Y, rear_center_z), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    front_plane = FLANGE_PLANE.offset(FLANGE_THICKNESS)
    front_outer_size = FUNNEL_FRONT_SIZE + 2 * CAGE_WALL
    outer = loft(
        [
            rear_plane * RectangleRounded(2 * CAGE_OUTER_HALF_WIDTH, rear_height, FUNNEL_REAR_CORNER_RADIUS),
            front_plane * RectangleRounded(front_outer_size, front_outer_size, FUNNEL_FRONT_CORNER_RADIUS + CAGE_WALL),
        ]
    )
    inner = loft(
        [
            rear_plane.offset(CUTTER_OVERLAP)
            * RectangleRounded(2 * CAGE_INNER_HALF_WIDTH, rear_height - 2 * CAGE_WALL, FUNNEL_REAR_INNER_CORNER_RADIUS),
            front_plane.offset(-CUTTER_OVERLAP)
            * RectangleRounded(FUNNEL_FRONT_SIZE, FUNNEL_FRONT_SIZE, FUNNEL_FRONT_CORNER_RADIUS),
        ]
    )
    return outer - inner


def _flange() -> Part:
    plate = FLANGE_PLANE.location * extrude(
        RectangleRounded(FAN_4010_SIZE, FAN_4010_SIZE, FLANGE_CORNER_RADIUS), FLANGE_THICKNESS
    )
    opening = FLANGE_PLANE.location * Cylinder(FUNNEL_FRONT_SIZE / 2, FLANGE_THICKNESS, align=BOTTOM)
    boss_radius = FAN_SCREW_BOSS_DIAMETER / 2
    bosses = [
        FLANGE_PLANE.location
        * Pos(x, y, FLANGE_THICKNESS)
        * (
            Cylinder(boss_radius, FAN_SCREW_BOSS_DEPTH, align=BOTTOM)
            + Pos(0, 0, FAN_SCREW_BOSS_DEPTH) * Cone(boss_radius, 0, boss_radius, align=BOTTOM)
        )
        for x, y in FAN_4010_MOUNTING_HOLES
    ]
    screw_holes = [
        FLANGE_PLANE.location
        * Pos(x, y, 0)
        * Cylinder(M3_PILOT_DIAMETER / 2, FLANGE_THICKNESS + FAN_SCREW_BOSS_DEPTH, align=BOTTOM)
        for x, y in FAN_4010_MOUNTING_HOLES
    ]
    return plate - opening + bosses - screw_holes


def _arm_path(end_y: float) -> Wire:
    front = Vector(HOTEND_AXIS_X, ARM_FRONT_Y, ARM_CENTER_Z)
    corner = front + Vector(ARM_SIDE_X_OFFSET, 0, 0)
    return FilletPolyline(front, corner, Vector(corner.X, end_y, ARM_CENTER_Z), radius=ARM_TURN_RADIUS)


def _arm(size: float, radius: float, end_y: float) -> Part:
    start = Plane(origin=(HOTEND_AXIS_X, ARM_FRONT_Y, ARM_CENTER_Z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return sweep(start * RectangleRounded(size, size, radius), _arm_path(end_y), transition=Transition.ROUND)


def _outlet(exit_half: float, entry_half: float, start: float, end: float, y_range: tuple[float, float]) -> Part:
    normal = Vector(-OUTLET_DIRECTION.Z, 0, OUTLET_DIRECTION.X)
    corners = [
        OUTLET_EXIT_CENTER + OUTLET_DIRECTION * start + normal * exit_half,
        OUTLET_EXIT_CENTER + OUTLET_DIRECTION * start - normal * exit_half,
        OUTLET_EXIT_CENTER - OUTLET_DIRECTION * end - normal * entry_half,
        OUTLET_EXIT_CENTER - OUTLET_DIRECTION * end + normal * entry_half,
    ]
    profile = Plane(origin=(0, y_range[1], 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0)) * Polygon(
        *[(corner.X, corner.Z) for corner in corners], align=None
    )
    return extrude(profile, y_range[1] - y_range[0], dir=(0, -1, 0))


def _right_duct_half() -> tuple[Part, Part]:
    outer = _arm(ARM_SIZE, ARM_CORNER_RADIUS, ARM_END_Y) + _outlet(
        OUTLET_GAP / 2 + DUCT_WALL, OUTLET_ENTRY_GAP / 2 + DUCT_WALL, 0, OUTLET_LENGTH, OUTLET_Y_RANGE
    )
    inner = _arm(ARM_SIZE - 2 * DUCT_WALL, ARM_CORNER_RADIUS - DUCT_WALL, ARM_END_Y - DUCT_WALL) + _outlet(
        OUTLET_GAP / 2,
        OUTLET_ENTRY_GAP / 2,
        CUT_OVERSHOOT,
        OUTLET_LENGTH - DUCT_WALL,
        (OUTLET_Y_RANGE[0] + DUCT_WALL, OUTLET_Y_RANGE[1] - DUCT_WALL),
    )
    side_x = (HOTEND_AXIS_X, HOTEND_AXIS_X + ARM_SIDE_X_OFFSET + ARM_SIZE)
    outer -= block(side_x, (NUT_STEP_FRONT_Y, CARRIAGE_PLATE_FRONT_Y), (NUT_STEP_TOP_Z, NUT_STEP_TOP_Z + ARM_SIZE))
    inner -= block(
        side_x,
        (NUT_STEP_FRONT_Y - DUCT_WALL, CARRIAGE_PLATE_FRONT_Y),
        (NUT_STEP_TOP_Z - DUCT_WALL, NUT_STEP_TOP_Z + ARM_SIZE),
    )
    return outer, inner


def _blower_socket() -> tuple[Part, Part]:
    socket_x = (-SOCKET_OUTER[0] / 2, SOCKET_OUTER[0] / 2)
    socket_down = (SOCKET_CENTER_DOWN - SOCKET_OUTER[1] / 2, SOCKET_CENTER_DOWN + SOCKET_OUTER[1] / 2)
    bottom_face_down = socket_down[1]
    clamp_bosses = [
        FLANGE_PLANE.location
        * Pos(x, bottom_face_down, CLAMP_SCREW_DEPTH)
        * Plane.XZ.rotated((180, 0, 0)).location
        * Cylinder(CLAMP_SCREW_BOSS_DIAMETER / 2, CLAMP_SCREW_BOSS_HEIGHT, align=BOTTOM)
        for x in CLAMP_SCREW_X_OFFSETS
    ]
    outer = _flange_box(socket_x, socket_down, (0, SOCKET_DEPTH + PLENUM_DEPTH)) + clamp_bosses
    pocket = _flange_box(
        (-SOCKET_INNER[0] / 2, SOCKET_INNER[0] / 2),
        (SOCKET_CENTER_DOWN - SOCKET_INNER[1] / 2, SOCKET_CENTER_DOWN + SOCKET_INNER[1] / 2),
        (0, SOCKET_DEPTH),
    )
    passage = _flange_box(
        (-PASSAGE[0] / 2, PASSAGE[0] / 2),
        (SOCKET_CENTER_DOWN - PASSAGE[1] / 2, SOCKET_CENTER_DOWN + PASSAGE[1] / 2),
        (SOCKET_DEPTH - CUTTER_OVERLAP, SOCKET_DEPTH + PLENUM_DEPTH - DUCT_WALL),
    )
    latch_window = _flange_box(
        (socket_x[0], -SOCKET_INNER[0] / 2),
        (
            BLOWER_FACE_DOWN + BLOWER_5015_LATCH_Z[0] - LATCH_WINDOW_CLEARANCE,
            BLOWER_FACE_DOWN + BLOWER_5015_LATCH_Z[1] + LATCH_WINDOW_CLEARANCE,
        ),
        (0, SOCKET_DEPTH - BLOWER_5015_LATCH_Y[0] + LATCH_WINDOW_CLEARANCE),
    )
    volute_relief = _flange_box(
        (SOCKET_INNER[0] / 2, socket_x[1]),
        (SOCKET_CENTER_DOWN - SOCKET_INNER[1] / 2, SOCKET_CENTER_DOWN + SOCKET_INNER[1] / 2),
        (0, VOLUTE_RELIEF_DEPTH),
    )
    clamp_holes = [
        FLANGE_PLANE.location
        * Pos(x, bottom_face_down + CLAMP_SCREW_BOSS_HEIGHT, CLAMP_SCREW_DEPTH)
        * Plane.XZ.location
        * Cylinder(M2_PILOT_DIAMETER / 2, CLAMP_SCREW_BOSS_HEIGHT + CAGE_WALL, align=BOTTOM)
        for x in CLAMP_SCREW_X_OFFSETS
    ]
    return outer, pocket + passage + latch_window + volute_relief + clamp_holes


def _duct() -> Part:
    right_outer, right_inner = _right_duct_half()
    mirror_plane = Plane.YZ.offset(HOTEND_AXIS_X)
    socket_outer, socket_inner = _blower_socket()
    outer = right_outer + mirror(right_outer, mirror_plane) + socket_outer
    inner = right_inner + mirror(right_inner, mirror_plane) + socket_inner
    return outer - inner


def hotend_shroud() -> Part:
    shroud = _cage() + _funnel() + _flange() + _duct()
    shroud -= _wheel_nut_clearance()
    shroud.label = "hotend_shroud"
    shroud.color = PRINTED_PART_COLOR
    return shroud


def hotend_shroud_for_printing() -> Part:
    return FLANGE_PLANE.location.inverse() * hotend_shroud()
