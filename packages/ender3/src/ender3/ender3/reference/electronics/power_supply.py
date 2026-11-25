from math import asin, degrees, radians, tan

from build123d import (
    Align,
    Axis,
    Box,
    Cone,
    Cylinder,
    Edge,
    Face,
    Part,
    Plane,
    Pos,
    Sketch,
    SlotArc,
    SlotCenterToCenter,
    extrude,
    fillet,
)

from ender3.construction import block
from ender3.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_BACK, FACE_RIGHT
from ender3.ender3.reference.construction import circles, outline_face
from ender3.ender3.reference.electronics.dimensions import (
    POWER_SUPPLY_BACK_TAPPED_HOLES,
    POWER_SUPPLY_FRONT_TAPPED_HOLES,
    POWER_SUPPLY_LOCATION,
    POWER_SUPPLY_SIZE,
)

POWER_SUPPLY_WALL_THICKNESS = 2.0
POWER_SUPPLY_EDGE_RADIUS = 2.0
POWER_SUPPLY_RECESS_OUTER_X_RANGE = (7.0, 27.0)
POWER_SUPPLY_RECESS_DEPTH = 2.5
POWER_SUPPLY_RECESS_OUTER_RADIUS = 5.0
POWER_SUPPLY_RECESS_INNER_RADIUS = 3.0
POWER_SUPPLY_TOP_RECESS_Y_RANGE = (28.0, 74.0)
POWER_SUPPLY_BACK_RECESS_Z_RANGE = (85.0, 117.0)
POWER_SUPPLY_FRONT_TAPPED_HOLE_DIAMETER = 3.3
POWER_SUPPLY_FRONT_TAPPED_HOLE_DEPTH = 10.1

POWER_SUPPLY_FRONT_BOSS_DIAMETER = 7.3
POWER_SUPPLY_FRONT_BOSS_LENGTH = 11.232
POWER_SUPPLY_BOSS_TIP_HALF_ANGLE = 59.0
POWER_SUPPLY_SIDE_TAPPED_HOLE_DIAMETER = 3.2
POWER_SUPPLY_SIDE_TAPPED_HOLE_DEPTH = 4.0
POWER_SUPPLY_SIDE_TAPPED_HOLES = [(32.0, 33.0), (82.0, 33.0), (32.0, 183.0), (82.0, 183.0)]
POWER_SUPPLY_SIDE_BOSS_DIAMETER = 7.2
POWER_SUPPLY_SIDE_BOSS_HEIGHT = 4.0
POWER_SUPPLY_BACK_TAPPED_HOLE_DIAMETER = 3.0
POWER_SUPPLY_BACK_TAPPED_HOLE_DEPTH = 4.0

POWER_SUPPLY_BACK_BOSS_DIAMETER = 7.0
POWER_SUPPLY_BACK_BOSS_HEIGHT = 4.0
POWER_SUPPLY_FAN_GRILLE_CENTER = (36.0, 168.0)
POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_RADIUS = 23.0
POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_WIDTH = 5.0
POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_GAP = 9.5
POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_RADIUS = 15.5
POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_WIDTH = 6.0
POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_HALF_SPAN = 30.0
POWER_SUPPLY_FAN_GRILLE_HOLE_DIAMETER = 4.0
POWER_SUPPLY_FAN_GRILLE_HOLE_OFFSET = 6.5
POWER_SUPPLY_FAN_SIDE_VENT_SLOT_WIDTH = 4.0
POWER_SUPPLY_FAN_SIDE_VENT_SLOT_CENTER_DISTANCE = 29.0
POWER_SUPPLY_FAN_SIDE_VENT_SLOT_CENTERS = [(y, z) for y in (33.5, 85.0) for z in (39.0, 47.0, 55.0)]
POWER_SUPPLY_CORNER_SLOT_WIDTH = 4.0
POWER_SUPPLY_CORNER_SLOT_Z = [62.0, 70.0]
POWER_SUPPLY_CORNER_SLOT_SIDE_END_Y = 108.0
POWER_SUPPLY_CORNER_SLOT_BACK_END_X = 20.0
POWER_SUPPLY_BACK_WINDOW_X_RANGE = (9.5, 18.5)
POWER_SUPPLY_BACK_WINDOW_Z_RANGE = (130.0, 144.0)
POWER_SUPPLY_BACK_SLOT_X_RANGE = (13.0, 20.0)
POWER_SUPPLY_BACK_SLOT_Z_RANGES = [(174.0, 176.0), (189.0, 191.0)]


def _left_rounded_rectangle(u_range: tuple[float, float], v_range: tuple[float, float], corner_radius: float) -> Face:
    (u0, u1), (v0, v1) = u_range, v_range
    return outline_face([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], [corner_radius, 0, 0, corner_radius])


def _power_supply_recess(outer_u: tuple[float, float], outer_v: tuple[float, float]) -> tuple[Face, Face]:
    wall = POWER_SUPPLY_WALL_THICKNESS
    (u0, u1), (v0, v1) = outer_u, outer_v
    outer = _left_rounded_rectangle(outer_u, outer_v, POWER_SUPPLY_RECESS_OUTER_RADIUS)
    inner = _left_rounded_rectangle((u0 + wall, u1 - wall), (v0 + wall, v1 - wall), POWER_SUPPLY_RECESS_INNER_RADIUS)
    return outer, inner


def power_supply() -> Part:
    dx, dy, dz = POWER_SUPPLY_SIZE
    wall = POWER_SUPPLY_WALL_THICKNESS
    depth = POWER_SUPPLY_RECESS_DEPTH
    case = Box(dx, dy, dz, align=Align.MIN)
    left_edges = case.edges().group_by(Axis.X)[0]
    case = fillet(left_edges - left_edges.group_by(Axis.Z)[0], POWER_SUPPLY_EDGE_RADIUS)
    case -= block((wall, dx - wall), (wall, dy - wall), (-CUT_OVERSHOOT, dz - wall))
    top_outer, top_inner = _power_supply_recess(POWER_SUPPLY_RECESS_OUTER_X_RANGE, POWER_SUPPLY_TOP_RECESS_Y_RANGE)
    case += Pos(0, 0, dz - depth - wall) * extrude(top_outer, depth)
    case -= Pos(0, 0, dz - depth) * extrude(top_inner, depth + CUT_OVERSHOOT)
    back_outer, back_inner = _power_supply_recess(POWER_SUPPLY_RECESS_OUTER_X_RANGE, POWER_SUPPLY_BACK_RECESS_Z_RANGE)
    case += extrude(Plane.XZ.offset(-(dy - depth - wall)) * back_outer, -depth)
    case -= extrude(Plane.XZ.offset(-(dy - depth)) * back_inner, -(depth + CUT_OVERSHOOT))
    exclusive = (False, False)
    top_opening_edges = (
        case.edges()
        .group_by(Axis.Z)[-1]
        .filter_by_position(Axis.Y, *POWER_SUPPLY_TOP_RECESS_Y_RANGE, inclusive=exclusive)
        .filter_by_position(Axis.X, *POWER_SUPPLY_RECESS_OUTER_X_RANGE, inclusive=exclusive)
    )
    back_opening_edges = (
        case.edges()
        .group_by(Axis.Y)[-1]
        .filter_by_position(Axis.Z, *POWER_SUPPLY_BACK_RECESS_Z_RANGE, inclusive=exclusive)
        .filter_by_position(Axis.X, *POWER_SUPPLY_RECESS_OUTER_X_RANGE, inclusive=exclusive)
    )
    far_side_edges = top_opening_edges.group_by(Axis.X)[-1] + back_opening_edges.group_by(Axis.X)[-1]
    case = fillet(top_opening_edges + back_opening_edges - far_side_edges, POWER_SUPPLY_WALL_THICKNESS)
    tip_slope = tan(radians(POWER_SUPPLY_BOSS_TIP_HALF_ANGLE))
    boss_radius = POWER_SUPPLY_FRONT_BOSS_DIAMETER / 2
    hole_radius = POWER_SUPPLY_FRONT_TAPPED_HOLE_DIAMETER / 2
    boss_length = POWER_SUPPLY_FRONT_BOSS_LENGTH - wall
    front_bosses = [
        Pos(x, wall, z)
        * FACE_BACK
        * (
            Cylinder(boss_radius, boss_length, align=BOTTOM)
            + Pos(0, 0, boss_length) * Cone(boss_radius, 0, boss_radius / tip_slope, align=BOTTOM)
        )
        for x, z in POWER_SUPPLY_FRONT_TAPPED_HOLES
    ]
    front_holes = [
        Pos(x, -CUT_OVERSHOOT, z)
        * FACE_BACK
        * (
            Cylinder(hole_radius, POWER_SUPPLY_FRONT_TAPPED_HOLE_DEPTH + CUT_OVERSHOOT, align=BOTTOM)
            + Pos(0, 0, POWER_SUPPLY_FRONT_TAPPED_HOLE_DEPTH + CUT_OVERSHOOT)
            * Cone(hole_radius, 0, hole_radius / tip_slope, align=BOTTOM)
        )
        for x, z in POWER_SUPPLY_FRONT_TAPPED_HOLES
    ]
    side_bosses = [
        Pos(wall, y, z)
        * FACE_RIGHT
        * Cylinder(POWER_SUPPLY_SIDE_BOSS_DIAMETER / 2, POWER_SUPPLY_SIDE_BOSS_HEIGHT, align=BOTTOM)
        for y, z in POWER_SUPPLY_SIDE_TAPPED_HOLES
    ]
    side_holes = [
        Pos(-CUT_OVERSHOOT, y, z)
        * FACE_RIGHT
        * Cylinder(
            POWER_SUPPLY_SIDE_TAPPED_HOLE_DIAMETER / 2,
            POWER_SUPPLY_SIDE_TAPPED_HOLE_DEPTH + CUT_OVERSHOOT,
            align=BOTTOM,
        )
        for y, z in POWER_SUPPLY_SIDE_TAPPED_HOLES
    ]
    back_bosses = [
        Pos(x, dy - wall - POWER_SUPPLY_BACK_BOSS_HEIGHT, z)
        * FACE_BACK
        * Cylinder(POWER_SUPPLY_BACK_BOSS_DIAMETER / 2, POWER_SUPPLY_BACK_BOSS_HEIGHT, align=BOTTOM)
        for x, z in POWER_SUPPLY_BACK_TAPPED_HOLES
    ]
    back_holes = [
        Pos(x, dy - POWER_SUPPLY_BACK_TAPPED_HOLE_DEPTH, z)
        * FACE_BACK
        * Cylinder(
            POWER_SUPPLY_BACK_TAPPED_HOLE_DIAMETER / 2,
            POWER_SUPPLY_BACK_TAPPED_HOLE_DEPTH + CUT_OVERSHOOT,
            align=BOTTOM,
        )
        for x, z in POWER_SUPPLY_BACK_TAPPED_HOLES
    ]
    outer_gap_angle = degrees(
        asin(POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_GAP / 2 / POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_RADIUS)
    )
    outer_slots = [
        SlotArc(
            Edge.make_circle(
                POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_RADIUS,
                start_angle=90 * k + outer_gap_angle,
                end_angle=90 * (k + 1) - outer_gap_angle,
            ),
            POWER_SUPPLY_FAN_GRILLE_OUTER_SLOT_WIDTH,
        )
        for k in range(4)
    ]
    half_span = POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_HALF_SPAN
    inner_slots = [
        SlotArc(
            Edge.make_circle(
                POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_RADIUS,
                start_angle=90 * k + 90 - half_span,
                end_angle=90 * k + 90 + half_span,
            ),
            POWER_SUPPLY_FAN_GRILLE_INNER_SLOT_WIDTH,
        )
        for k in range(4)
    ]
    offset = POWER_SUPPLY_FAN_GRILLE_HOLE_OFFSET
    grille_holes = circles(
        [(offset, 0), (-offset, 0), (0, offset), (0, -offset)], POWER_SUPPLY_FAN_GRILLE_HOLE_DIAMETER
    )
    grille = Pos(*POWER_SUPPLY_FAN_GRILLE_CENTER) * (Sketch() + outer_slots + inner_slots + grille_holes)
    vents = [
        Pos(y, z)
        * SlotCenterToCenter(POWER_SUPPLY_FAN_SIDE_VENT_SLOT_CENTER_DISTANCE, POWER_SUPPLY_FAN_SIDE_VENT_SLOT_WIDTH)
        for y, z in POWER_SUPPLY_FAN_SIDE_VENT_SLOT_CENTERS
    ]
    fan_side_cutouts = extrude(Plane.YZ.offset(dx - wall - CUT_OVERSHOOT / 2) * (grille + vents), wall + CUT_OVERSHOOT)
    slot_half = POWER_SUPPLY_CORNER_SLOT_WIDTH / 2
    side_end_y = POWER_SUPPLY_CORNER_SLOT_SIDE_END_Y
    back_end_x = POWER_SUPPLY_CORNER_SLOT_BACK_END_X
    back_wall_cut_y_range = (dy - wall - CUT_OVERSHOOT, dy + CUT_OVERSHOOT)
    corner_slots = [
        block((-CUT_OVERSHOOT, wall + CUT_OVERSHOOT), (side_end_y, dy + CUT_OVERSHOOT), (z - slot_half, z + slot_half))
        + Pos(-CUT_OVERSHOOT, side_end_y, z) * FACE_RIGHT * Cylinder(slot_half, wall + 2 * CUT_OVERSHOOT, align=BOTTOM)
        + block((-CUT_OVERSHOOT, back_end_x), back_wall_cut_y_range, (z - slot_half, z + slot_half))
        + Pos(back_end_x, dy - wall - CUT_OVERSHOOT, z)
        * FACE_BACK
        * Cylinder(slot_half, wall + 2 * CUT_OVERSHOOT, align=BOTTOM)
        for z in POWER_SUPPLY_CORNER_SLOT_Z
    ]
    back_cutouts = [
        block(POWER_SUPPLY_BACK_WINDOW_X_RANGE, back_wall_cut_y_range, POWER_SUPPLY_BACK_WINDOW_Z_RANGE),
        *(
            block(POWER_SUPPLY_BACK_SLOT_X_RANGE, back_wall_cut_y_range, z_range)
            for z_range in POWER_SUPPLY_BACK_SLOT_Z_RANGES
        ),
    ]
    case = case + front_bosses + side_bosses + back_bosses
    case = case - front_holes - side_holes - back_holes - fan_side_cutouts - corner_slots - back_cutouts
    case = POWER_SUPPLY_LOCATION * case
    case.label = "power_supply"
    return case
