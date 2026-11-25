from build123d import Cylinder, Part, Pos

from ender3.construction import block
from ender3.dimensions import BOTTOM, FACE_BACK, FACE_RIGHT
from ender3.upgrades.belt_tensioners.dimensions import (
    CASE_END_WALL_INNER_U_ABOVE_TRAVEL_MAX,
    CASE_END_WALL_THICKNESS,
    CASE_HALF_HEIGHT,
    CASE_INNER_HALF_HEIGHT,
    CASE_SIDE_WALL_INNER_W,
    CASE_W_RANGE,
    IDLER_STACK_WIDTH,
    STEM_MAJOR_DIAMETER,
)

CASE_COLLAR_THICKNESS = 3.0
CASE_WINDOW_SIDE_CLEARANCE = 0.5
CASE_WINDOW_HALF_WIDTH = IDLER_STACK_WIDTH / 2 + CASE_WINDOW_SIDE_CLEARANCE
STEM_HOLE_CLEARANCE = 1.0
STEM_HOLE_DIAMETER = STEM_MAJOR_DIAMETER + STEM_HOLE_CLEARANCE


def hole_along_w(u: float, v: float, diameter: float, w_range: tuple[float, float]) -> Part:
    return Pos(u, w_range[0], v) * FACE_BACK * Cylinder(diameter / 2, w_range[1] - w_range[0], align=BOTTOM)


def end_wall_u_range(travel: tuple[float, float]) -> tuple[float, float]:
    inner = CASE_END_WALL_INNER_U_ABOVE_TRAVEL_MAX + travel[1]
    return inner, inner + CASE_END_WALL_THICKNESS


def stem_hole(travel: tuple[float, float]) -> Part:
    end_wall = end_wall_u_range(travel)
    return Pos(end_wall[0], 0, 0) * FACE_RIGHT * Cylinder(STEM_HOLE_DIAMETER / 2, CASE_END_WALL_THICKNESS, align=BOTTOM)


def case_channel(start_u: float, travel: tuple[float, float]) -> Part:
    end_wall = end_wall_u_range(travel)
    length = (start_u, end_wall[1])
    channel = block(length, (CASE_W_RANGE[0], CASE_SIDE_WALL_INNER_W), (-CASE_HALF_HEIGHT, CASE_HALF_HEIGHT))
    channel += block(length, CASE_W_RANGE, (CASE_INNER_HALF_HEIGHT, CASE_HALF_HEIGHT))
    channel += block(length, CASE_W_RANGE, (-CASE_HALF_HEIGHT, -CASE_INNER_HALF_HEIGHT))
    channel += block(end_wall, CASE_W_RANGE, (-CASE_HALF_HEIGHT, CASE_HALF_HEIGHT))
    channel += block(
        (start_u, start_u + CASE_COLLAR_THICKNESS), CASE_W_RANGE, (-CASE_HALF_HEIGHT, CASE_HALF_HEIGHT)
    ) - block(
        (start_u, start_u + CASE_COLLAR_THICKNESS),
        (-CASE_WINDOW_HALF_WIDTH, CASE_WINDOW_HALF_WIDTH),
        (-CASE_INNER_HALF_HEIGHT, CASE_INNER_HALF_HEIGHT),
    )
    return channel
