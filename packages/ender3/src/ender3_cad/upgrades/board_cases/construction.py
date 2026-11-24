from build123d import Circle, Cylinder, Part, Plane, Polygon, Pos, Rectangle, Sketch, Vector, extrude, mirror

from ender3_cad.construction import block
from ender3_cad.dimensions import (
    BOTTOM,
    CUT_OVERSHOOT,
    FACE_BACK,
    M3_CLEARANCE_DIAMETER,
    M3_HEAT_SET_INSERT_DEPTH,
    M3_HEAT_SET_INSERT_HOLE_DIAMETER,
    M5_CLEARANCE_DIAMETER,
)
from ender3_cad.ender3.reference.components.dimensions import FAN_4010_MOUNTING_HOLES
from ender3_cad.upgrades.board_cases.dimensions import (
    CEILING_BOTTOM_Z,
    CEILING_TOP_Z,
    DRAWER_BACK_Y,
    DRAWER_FRONT_Y,
    HEAT_SET_INSERT_WALL,
    LEFT_INNER_X,
    LEFT_OUTER_X,
    LEFT_PANEL_OUTER_X,
    LEFT_PANEL_SCREW_HOLES,
    LEFT_TRAY_SCREW_POINTS,
    PANEL_FRONT_Y,
    PANEL_THICKNESS,
    RAIL_SLOT_CENTERS_Z,
    TRAY_BOTTOM_Z,
    TRAY_SCREW_COLUMN_SIZE,
    TRAY_THICKNESS,
    TRAY_TOP_Z,
    WALL_THICKNESS,
)
from ender3_cad.upgrades.construction import t_rail

M3_SELF_TAPPING_DIAMETER = 2.9

EXHAUST_SLOT_WIDTH = 3.0
EXHAUST_SLOT_Z = (14.0, 27.0)
EXHAUST_SLOT_PITCH = 6.0
EXHAUST_SLOT_COUNT = 17
EXHAUST_SLOT_FIRST_Y = -142.0
EXHAUST_SLOT_CENTERS_Y = [EXHAUST_SLOT_FIRST_Y + i * EXHAUST_SLOT_PITCH for i in range(EXHAUST_SLOT_COUNT)]

UART_NOTCH_Y = (-64.0, -56.0)
UART_NOTCH_HEIGHT = 10.0

PORT_POCKET_MARGIN = 3.0
PANEL_SKIN_THICKNESS = 1.2
PORT_POCKET_DEPTH = PANEL_THICKNESS - PANEL_SKIN_THICKNESS
PORT_POCKET_FLOOR_Y = PANEL_FRONT_Y + PORT_POCKET_DEPTH

FAN_BOSS_DIAMETER = 5.5
FAN_BOSS_HEIGHT = 3.5
INTAKE_GRILLE_DIAMETER = 36.0
INTAKE_GRILLE_SLOT_WIDTH = 3.0
INTAKE_GRILLE_SLOT_OFFSETS = [-15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0]


def standoffs_and_insert_holes(
    points: list[Vector], insert_hole_diameter: float, insert_depth: float, bottom_z: float
) -> tuple[list[Part], list[Part]]:
    radius = insert_hole_diameter / 2 + HEAT_SET_INSERT_WALL
    posts = [Pos(p.X, p.Y, bottom_z) * Cylinder(radius, CEILING_BOTTOM_Z - bottom_z, align=BOTTOM) for p in points]
    insert_holes = [
        Pos(p.X, p.Y, bottom_z) * Cylinder(insert_hole_diameter / 2, insert_depth, align=BOTTOM) for p in points
    ]
    return posts, insert_holes


def front_port_cutouts(openings: list[tuple[tuple[float, float], tuple[float, float]]]) -> list[Part]:
    cutouts = []
    for (x0, x1), (z0, z1) in openings:
        pocket_top_z = z1 + PORT_POCKET_MARGIN
        pocket_bottom_z = z0 - PORT_POCKET_MARGIN
        pocket_profile = Polygon(
            (PANEL_FRONT_Y - CUT_OVERSHOOT, pocket_top_z),
            (PORT_POCKET_FLOOR_Y, pocket_top_z),
            (PORT_POCKET_FLOOR_Y, pocket_bottom_z),
            (PANEL_FRONT_Y, pocket_bottom_z - PORT_POCKET_DEPTH),
            (PANEL_FRONT_Y - CUT_OVERSHOOT, pocket_bottom_z - PORT_POCKET_DEPTH),
            align=None,
        )
        pocket_width = x1 - x0 + 2 * PORT_POCKET_MARGIN
        cutouts += [
            Pos(x0 - PORT_POCKET_MARGIN, 0, 0) * extrude(Plane.YZ * pocket_profile, pocket_width, dir=(1, 0, 0)),
            block((x0, x1), (PANEL_FRONT_Y - CUT_OVERSHOOT, DRAWER_FRONT_Y + CUT_OVERSHOOT), (z0, z1)),
        ]
    return cutouts


def left_shell() -> Part:
    x_range = (LEFT_OUTER_X, LEFT_INNER_X)
    box = block(x_range, (DRAWER_FRONT_Y, DRAWER_BACK_Y), (TRAY_TOP_Z, CEILING_TOP_Z))
    cavity = block(
        (LEFT_OUTER_X + WALL_THICKNESS, LEFT_INNER_X - WALL_THICKNESS),
        (DRAWER_FRONT_Y, DRAWER_BACK_Y - WALL_THICKNESS),
        (TRAY_TOP_Z, CEILING_BOTTOM_Z),
    )
    panel = block((LEFT_PANEL_OUTER_X, LEFT_INNER_X), (PANEL_FRONT_Y, DRAWER_FRONT_Y), (TRAY_BOTTOM_Z, CEILING_TOP_Z))
    t_rails = [mirror(t_rail(slot_z, (DRAWER_FRONT_Y, DRAWER_BACK_Y)), Plane.YZ) for slot_z in RAIL_SLOT_CENTERS_Z]
    half = TRAY_SCREW_COLUMN_SIZE / 2
    screw_columns = [
        block((x - half, x + half), (y - half, y + half), (TRAY_TOP_Z, CEILING_BOTTOM_Z))
        for x, y in LEFT_TRAY_SCREW_POINTS
    ]
    tray_insert_holes = [
        Pos(x, y, TRAY_TOP_Z) * Cylinder(M3_HEAT_SET_INSERT_HOLE_DIAMETER / 2, M3_HEAT_SET_INSERT_DEPTH, align=BOTTOM)
        for x, y in LEFT_TRAY_SCREW_POINTS
    ]
    panel_screw_holes = [
        Pos(x, PANEL_FRONT_Y, z) * FACE_BACK * Cylinder(M5_CLEARANCE_DIAMETER / 2, PANEL_THICKNESS, align=BOTTOM)
        for x, z in LEFT_PANEL_SCREW_HOLES
    ]
    inner_wall_x = (LEFT_INNER_X - WALL_THICKNESS, LEFT_INNER_X)
    exhaust_slots = [
        block(inner_wall_x, (y - EXHAUST_SLOT_WIDTH / 2, y + EXHAUST_SLOT_WIDTH / 2), EXHAUST_SLOT_Z)
        for y in EXHAUST_SLOT_CENTERS_Y
    ]
    uart_notch = block(inner_wall_x, UART_NOTCH_Y, (TRAY_TOP_Z, TRAY_TOP_Z + UART_NOTCH_HEIGHT))
    shell = box - cavity + panel + t_rails + screw_columns
    return shell - tray_insert_holes - panel_screw_holes - exhaust_slots - uart_notch


def floor_tray(
    x_range: tuple[float, float], screw_points: list[tuple[float, float]], fan_center: tuple[float, float]
) -> Part:
    fan_x, fan_y = fan_center
    plate = block(x_range, (DRAWER_FRONT_Y, DRAWER_BACK_Y), (TRAY_BOTTOM_Z, TRAY_TOP_Z))
    fan_bosses = [
        Pos(fan_x + x, fan_y + y, TRAY_TOP_Z) * Cylinder(FAN_BOSS_DIAMETER / 2, FAN_BOSS_HEIGHT, align=BOTTOM)
        for x, y in FAN_4010_MOUNTING_HOLES
    ]
    fan_screw_holes = [
        Pos(fan_x + x, fan_y + y, TRAY_BOTTOM_Z)
        * Cylinder(M3_SELF_TAPPING_DIAMETER / 2, TRAY_THICKNESS + FAN_BOSS_HEIGHT, align=BOTTOM)
        for x, y in FAN_4010_MOUNTING_HOLES
    ]
    tray_screw_holes = [
        Pos(x, y, TRAY_BOTTOM_Z) * Cylinder(M3_CLEARANCE_DIAMETER / 2, TRAY_THICKNESS, align=BOTTOM)
        for x, y in screw_points
    ]
    grille_slots = Sketch() + [
        Pos(0, offset) * Rectangle(INTAKE_GRILLE_DIAMETER, INTAKE_GRILLE_SLOT_WIDTH)
        for offset in INTAKE_GRILLE_SLOT_OFFSETS
    ]
    intake_grille = Pos(fan_x, fan_y, TRAY_BOTTOM_Z) * extrude(
        Circle(INTAKE_GRILLE_DIAMETER / 2) & grille_slots, TRAY_THICKNESS
    )
    return plate + fan_bosses - fan_screw_holes - tray_screw_holes - intake_grille
