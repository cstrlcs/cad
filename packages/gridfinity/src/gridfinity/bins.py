from build123d import Align, Box, Part, Pos, RectangleRounded, extrude

from gridfinity.spec import (
    BASE_HEIGHT,
    BIN_BASE_PROFILE,
    BIN_FLOOR_TOP_Z,
    BIN_GAP,
    BIN_OUTER_RADIUS,
    BIN_UNIT_SIZE,
    GRID_PITCH,
    HEIGHT_UNIT,
    MIN_CORNER,
    STACKING_LIP_DEPTH,
    STACKING_LIP_HEIGHT,
    STACKING_LIP_PROFILE,
    profiled_block,
)

WALL_THICKNESS = 1.9
DIVIDER_THICKNESS = 1.5
DIVIDER_TOP_BELOW_RIM = 1.0
MIN_HEIGHT_UNITS = 2


def bin_size(units_x: int, units_y: int, height_units: int) -> tuple[float, float, float]:
    return units_x * GRID_PITCH - BIN_GAP, units_y * GRID_PITCH - BIN_GAP, height_units * HEIGHT_UNIT


def weighted_spans(start: float, end: float, weights: tuple[float, ...]) -> list[tuple[float, float]]:
    usable = end - start - (len(weights) - 1) * DIVIDER_THICKNESS
    spans = []
    low = start
    for weight in weights:
        high = low + usable * weight / sum(weights)
        spans.append((low, high))
        low = high + DIVIDER_THICKNESS
    return spans


def dividers_between(spans: list[tuple[float, float]]) -> list[float]:
    return [high for _, high in spans[:-1]]


def divider_along_x(y: float, x_range: tuple[float, float], rim_z: float) -> Part:
    x0, x1 = x_range
    return Pos(x0, y, BIN_FLOOR_TOP_Z) * Box(
        x1 - x0, DIVIDER_THICKNESS, rim_z - DIVIDER_TOP_BELOW_RIM - BIN_FLOOR_TOP_Z, align=Align.MIN
    )


def divider_along_y(x: float, y_range: tuple[float, float], rim_z: float) -> Part:
    y0, y1 = y_range
    return Pos(x, y0, BIN_FLOOR_TOP_Z) * Box(
        DIVIDER_THICKNESS, y1 - y0, rim_z - DIVIDER_TOP_BELOW_RIM - BIN_FLOOR_TOP_Z, align=Align.MIN
    )


def _outline(width: float, length: float, inset: float) -> RectangleRounded:
    return Pos(width / 2, length / 2) * RectangleRounded(
        width - 2 * inset, length - 2 * inset, BIN_OUTER_RADIUS - inset
    )


def _cavity(width: float, length: float, rim_z: float) -> Part:
    support_height = STACKING_LIP_DEPTH - WALL_THICKNESS
    support_bottom_z = rim_z - support_height
    cavity = Pos(0, 0, BIN_FLOOR_TOP_Z) * extrude(
        _outline(width, length, WALL_THICKNESS), support_bottom_z - BIN_FLOOR_TOP_Z
    )
    cavity += Pos(0, 0, support_bottom_z) * extrude(_outline(width, length, WALL_THICKNESS), support_height, taper=45)
    cavity += Pos(width / 2, length / 2, rim_z) * profiled_block(width, length, BIN_OUTER_RADIUS, STACKING_LIP_PROFILE)
    cavity += Pos(0, 0, rim_z + STACKING_LIP_HEIGHT) * extrude(_outline(width, length, 0), STACKING_LIP_HEIGHT)
    return cavity


def _equal_dividers(span: float, count: int) -> list[float]:
    return dividers_between(weighted_spans(WALL_THICKNESS, span - WALL_THICKNESS, (1.0,) * count))


def gridfinity_bin(
    units_x: int, units_y: int, height_units: int, compartments_x: int = 1, compartments_y: int = 1
) -> Part:
    if height_units < MIN_HEIGHT_UNITS:
        message = f"height_units must be at least {MIN_HEIGHT_UNITS}, got {height_units}"
        raise ValueError(message)
    width, length, rim_z = bin_size(units_x, units_y, height_units)
    foot = profiled_block(BIN_UNIT_SIZE, BIN_UNIT_SIZE, BIN_OUTER_RADIUS, BIN_BASE_PROFILE)
    feet = [
        Pos(BIN_UNIT_SIZE / 2 + i * GRID_PITCH, BIN_UNIT_SIZE / 2 + j * GRID_PITCH, 0) * foot
        for i in range(units_x)
        for j in range(units_y)
    ]
    body = Pos(0, 0, BASE_HEIGHT) * extrude(
        RectangleRounded(width, length, BIN_OUTER_RADIUS, align=MIN_CORNER),
        rim_z + STACKING_LIP_HEIGHT - BASE_HEIGHT,
    )
    dividers_x = [
        divider_along_y(x, (WALL_THICKNESS / 2, length - WALL_THICKNESS / 2), rim_z)
        for x in _equal_dividers(width, compartments_x)
    ]
    dividers_y = [
        divider_along_x(y, (WALL_THICKNESS / 2, width - WALL_THICKNESS / 2), rim_z)
        for y in _equal_dividers(length, compartments_y)
    ]
    storage_bin = body + feet - _cavity(width, length, rim_z) + dividers_x + dividers_y
    storage_bin.label = f"bin_{units_x}x{units_y}x{height_units}_{compartments_x}x{compartments_y}"
    return storage_bin
