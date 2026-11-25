from collections.abc import Callable
from math import cos, pi, radians, sin

from build123d import Cone, Cylinder, Location, Part, Plane, Pos, Rot, Vector

from ender3.construction import block
from ender3.dimensions import BOTTOM, FACE_RIGHT
from ender3.upgrades.x_cable_chain.dimensions import (
    BEND_RADIUS,
    CHAIN_AXIS_Z,
    FIXED_MOUNT_PIVOT_X,
    FIXED_RUN_Y,
    INNER_PLATE_X,
    INNER_ZONE_END_Y,
    LINK_COUNT,
    LINK_HEIGHT,
    LINK_PITCH,
    MOVING_RUN_Y,
    OUTER_PLATE_X,
    OUTER_ZONE_START_Y,
    PIVOT_Z,
    PLATE_CLEARANCE,
    PLATE_THICKNESS,
    ROTATION_GAP,
)

PIN_DIAMETER = 3.0
PIN_HOLE_DIAMETER = 3.4
PIN_TIP_CHAMFER = 0.4
PIN_ENGAGEMENT = 0.8
MAX_BEND_ANGLE = 45.0
BEND_STOP_TOOTH_LENGTH = (PIVOT_Z + ROTATION_GAP - PIVOT_Z * sin(radians(MAX_BEND_ANGLE))) / cos(
    radians(MAX_BEND_ANGLE)
)
BEND_STOP_CONTACT_Z = (
    PIVOT_Z + BEND_STOP_TOOTH_LENGTH * sin(radians(MAX_BEND_ANGLE)) - PIVOT_Z * cos(radians(MAX_BEND_ANGLE))
)
BEND_STOP_LIP_DEPTH = 0.3
BISECTION_STEPS = 40


def _x_cylinder(y: float, z: float, radius: float, x_range: tuple[float, float]) -> Part:
    return Pos(x_range[0], y, z) * FACE_RIGHT * Cylinder(radius, x_range[1] - x_range[0], align=BOTTOM)


def mirrored_x_ranges(inner_x: float, width: float) -> list[tuple[float, float]]:
    return [(-inner_x - width, -inner_x), (inner_x, inner_x + width)]


def stop_joints() -> list[Part]:
    joints = [
        block(x_range, (INNER_ZONE_END_Y, OUTER_ZONE_START_Y), (0, LINK_HEIGHT))
        for x_range in mirrored_x_ranges(INNER_PLATE_X, OUTER_PLATE_X + PLATE_THICKNESS - INNER_PLATE_X)
    ]
    lips = [
        block(
            x_range, (OUTER_ZONE_START_Y, OUTER_ZONE_START_Y + BEND_STOP_LIP_DEPTH), (BEND_STOP_CONTACT_Z, LINK_HEIGHT)
        )
        for x_range in mirrored_x_ranges(INNER_PLATE_X, PLATE_THICKNESS)
    ]
    return joints + lips


def female_end(start_y: float) -> Part:
    plates = [
        block(x_range, (start_y, 0), (0, LINK_HEIGHT)) + _x_cylinder(0, PIVOT_Z, PIVOT_Z, x_range)
        for x_range in mirrored_x_ranges(OUTER_PLATE_X, PLATE_THICKNESS)
    ]
    holes = _x_cylinder(
        0, PIVOT_Z, PIN_HOLE_DIAMETER / 2, (-OUTER_PLATE_X - PLATE_THICKNESS, OUTER_PLATE_X + PLATE_THICKNESS)
    )
    return Part() + plates - holes


def male_end(end_y: float) -> Part:
    plates = [
        block(x_range, (0, end_y), (0, LINK_HEIGHT))
        + _x_cylinder(0, PIVOT_Z, PIVOT_Z, x_range)
        + block(x_range, (-PIVOT_Z, 0), (PIVOT_Z, LINK_HEIGHT))
        + block(x_range, (-BEND_STOP_TOOTH_LENGTH, 0), (0, PIVOT_Z))
        for x_range in mirrored_x_ranges(INNER_PLATE_X, PLATE_THICKNESS)
    ]
    pin_length = PLATE_CLEARANCE + PIN_ENGAGEMENT
    pin_shaft = pin_length - PIN_TIP_CHAMFER
    pin = FACE_RIGHT * (
        Cylinder(PIN_DIAMETER / 2, pin_shaft, align=BOTTOM)
        + Pos(0, 0, pin_shaft)
        * Cone(PIN_DIAMETER / 2, PIN_DIAMETER / 2 - PIN_TIP_CHAMFER, PIN_TIP_CHAMFER, align=BOTTOM)
    )
    pins = [
        Pos(INNER_PLATE_X + PLATE_THICKNESS, 0, PIVOT_Z) * pin,
        Pos(-INNER_PLATE_X - PLATE_THICKNESS, 0, PIVOT_Z) * Rot(0, 0, 180) * pin,
    ]
    return Part() + plates + pins


def chain_frame(pivot: Vector, heading: Vector) -> Location:
    x_dir = Vector(0, 0, 1)
    z_dir = x_dir.cross(heading)
    return Plane(origin=pivot - z_dir * PIVOT_Z, x_dir=x_dir, z_dir=z_dir).location


def _path_point(distance: float, bend_x: float) -> Vector:
    first_run = bend_x - FIXED_MOUNT_PIVOT_X
    bend_length = pi * BEND_RADIUS
    center_y = (FIXED_RUN_Y + MOVING_RUN_Y) / 2
    if distance <= first_run:
        return Vector(FIXED_MOUNT_PIVOT_X + distance, FIXED_RUN_Y, CHAIN_AXIS_Z)
    if distance >= first_run + bend_length:
        return Vector(bend_x - (distance - first_run - bend_length), MOVING_RUN_Y, CHAIN_AXIS_Z)
    angle = (distance - first_run) / BEND_RADIUS
    return Vector(bend_x + BEND_RADIUS * sin(angle), center_y + BEND_RADIUS * cos(angle), CHAIN_AXIS_Z)


def _bisect(low: float, high: float, is_below: Callable[[float], bool]) -> float:
    for _ in range(BISECTION_STEPS):
        middle = (low + high) / 2
        if is_below(middle):
            low = middle
            continue
        high = middle
    return (low + high) / 2


def _next_pivot_distance(previous: Vector, distance: float, bend_x: float) -> float:
    return _bisect(
        distance,
        distance + 2 * LINK_PITCH,
        lambda candidate: (_path_point(candidate, bend_x) - previous).length < LINK_PITCH,
    )


def _walk_pivots(bend_x: float) -> list[Vector]:
    pivots = [Vector(FIXED_MOUNT_PIVOT_X, FIXED_RUN_Y, CHAIN_AXIS_Z)]
    distance = 0.0
    for _ in range(LINK_COUNT):
        distance = _next_pivot_distance(pivots[-1], distance, bend_x)
        pivots.append(_path_point(distance, bend_x))
    return pivots


def chain_pivots(moving_pivot_x: float) -> list[Vector]:
    bend_x = _bisect(
        moving_pivot_x,
        FIXED_MOUNT_PIVOT_X + LINK_COUNT * LINK_PITCH,
        lambda candidate: moving_pivot_x > _walk_pivots(candidate)[-1].X,
    )
    return _walk_pivots(bend_x)
