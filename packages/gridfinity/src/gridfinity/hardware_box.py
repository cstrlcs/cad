from typing import NamedTuple

from build123d import Align, Box, Cylinder, Location, Part, Pos, RectangleRounded, Rot, Text, extrude

from gridfinity.bins import (
    DIVIDER_THICKNESS,
    DIVIDER_TOP_BELOW_RIM,
    WALL_THICKNESS,
    bin_size,
    divider_along_x,
    divider_along_y,
    dividers_between,
    gridfinity_bin,
    weighted_spans,
)
from gridfinity.spec import (
    BIN_FLOOR_TOP_Z,
    BIN_OUTER_RADIUS,
    MIN_CORNER,
    STACKING_LIP_DEPTH,
    STACKING_LIP_HEIGHT,
    STACKING_LIP_PROFILE,
    profiled_block,
)

THREAD_SIZE_COLUMNS = (("M2", 0.8), ("M3", 1.0), ("M4", 1.1), ("M5", 1.2))
ROW_LENGTH_WEIGHTS = (1.7, 1.0, 1.0)

PEN_DIAMETER = 12.0
PEN_CHANNEL_WIDTH = 17.0
PEN_TOP_ABOVE_RIM = 2.0
PEN_CRADLE_CLEARANCE = 0.5

LID_CLEARANCE = 0.25
LID_PLATE_THICKNESS = 2.0
LID_SKIRT_THICKNESS = 1.2
LID_SKIRT_INNER_RADIUS = 1.0
LID_RIB_THICKNESS = 1.2
LID_RIB_GAP_ABOVE_DIVIDERS = 0.5

LATCH_RADIUS = 0.9
LATCH_PROTRUSION = 0.6
LATCH_LENGTH = 24.0
LATCH_GROOVE_CLEARANCE = 0.1
LATCH_Z_ABOVE_RIM = 1.6

GRIP_RADIUS = 5.0
GRIP_DEPTH = 3.0

LABEL_FONT_SIZE = 7.0
LABEL_DEPTH = 0.6

LID_SKIRT_OUTER_INSET = STACKING_LIP_DEPTH + LID_CLEARANCE
LATCH_AXIS_INSET = WALL_THICKNESS + LID_CLEARANCE + LATCH_RADIUS - LATCH_PROTRUSION


class Layout(NamedTuple):
    columns: list[tuple[float, float]]
    rows: list[tuple[float, float]]
    pen_divider_y: float
    column_dividers_x: list[float]
    row_dividers_y: list[float]


def _layout(width: float, length: float) -> Layout:
    pen_divider_y = WALL_THICKNESS + PEN_CHANNEL_WIDTH
    columns = weighted_spans(WALL_THICKNESS, width - WALL_THICKNESS, tuple(weight for _, weight in THREAD_SIZE_COLUMNS))
    rows = weighted_spans(pen_divider_y + DIVIDER_THICKNESS, length - WALL_THICKNESS, ROW_LENGTH_WEIGHTS)
    return Layout(columns, rows, pen_divider_y, dividers_between(columns), [pen_divider_y, *dividers_between(rows)])


def _lid_flip(length: float, rim_z: float) -> Location:
    return Pos(0, length, rim_z + STACKING_LIP_HEIGHT + LID_PLATE_THICKNESS) * Rot(180, 0, 0)


def _latches(width: float, length: float, rim_z: float, radius: float, latch_length: float) -> list[Part]:
    latch = Cylinder(radius, latch_length, rotation=(0, 90, 0))
    return [Pos(width / 2, y, rim_z + LATCH_Z_ABOVE_RIM) * latch for y in (LATCH_AXIS_INSET, length - LATCH_AXIS_INSET)]


def hardware_box(units_x: int, units_y: int, height_units: int) -> Part:
    width, length, rim_z = bin_size(units_x, units_y, height_units)
    layout = _layout(width, length)
    row_dividers = [
        divider_along_x(y, (WALL_THICKNESS / 2, width - WALL_THICKNESS / 2), rim_z) for y in layout.row_dividers_y
    ]
    column_dividers = [
        divider_along_y(x, (layout.pen_divider_y, length - WALL_THICKNESS / 2), rim_z) for x in layout.column_dividers_x
    ]
    pen_axis_y = WALL_THICKNESS + PEN_CHANNEL_WIDTH / 2
    pen_axis_z = rim_z + PEN_TOP_ABOVE_RIM - PEN_DIAMETER / 2
    cradle = Pos(WALL_THICKNESS, WALL_THICKNESS, BIN_FLOOR_TOP_Z) * Box(
        width - 2 * WALL_THICKNESS, PEN_CHANNEL_WIDTH, pen_axis_z - BIN_FLOOR_TOP_Z, align=Align.MIN
    )
    cradle -= Pos(width / 2, pen_axis_y, pen_axis_z) * Cylinder(
        PEN_DIAMETER / 2 + PEN_CRADLE_CLEARANCE, width, rotation=(0, 90, 0)
    )
    top_z = rim_z + STACKING_LIP_HEIGHT
    grip = Cylinder(GRIP_RADIUS, 2 * STACKING_LIP_DEPTH, rotation=(0, 90, 0))
    grips = [Pos(x, length / 2, top_z + GRIP_RADIUS - GRIP_DEPTH) * grip for x in (0, width)]
    box = gridfinity_bin(units_x, units_y, height_units) + row_dividers + column_dividers + cradle
    box -= (
        _latches(
            width,
            length,
            rim_z,
            LATCH_RADIUS + LATCH_GROOVE_CLEARANCE,
            LATCH_LENGTH + 2 * (LID_CLEARANCE + LATCH_GROOVE_CLEARANCE),
        )
        + grips
    )
    box.label = f"hardware_box_{units_x}x{units_y}x{height_units}"
    return box


def closed_lid_location(units_x: int, units_y: int, height_units: int) -> Location:
    _, length, rim_z = bin_size(units_x, units_y, height_units)
    return _lid_flip(length, rim_z)


def hardware_box_lid(units_x: int, units_y: int, height_units: int) -> Part:
    width, length, rim_z = bin_size(units_x, units_y, height_units)
    layout = _layout(width, length)
    top_z = rim_z + STACKING_LIP_HEIGHT
    plate = Pos(0, 0, top_z) * extrude(
        RectangleRounded(width, length, BIN_OUTER_RADIUS, align=MIN_CORNER), LID_PLATE_THICKNESS
    )
    skirt_inner_inset = LID_SKIRT_OUTER_INSET + LID_SKIRT_THICKNESS
    skirt = profiled_block(
        width - 2 * LID_CLEARANCE, length - 2 * LID_CLEARANCE, BIN_OUTER_RADIUS - LID_CLEARANCE, STACKING_LIP_PROFILE
    ) - extrude(
        RectangleRounded(width - 2 * skirt_inner_inset, length - 2 * skirt_inner_inset, LID_SKIRT_INNER_RADIUS),
        STACKING_LIP_HEIGHT,
    )
    skirt = Pos(width / 2, length / 2, rim_z) * skirt
    rib_bottom_z = rim_z - DIVIDER_TOP_BELOW_RIM + LID_RIB_GAP_ABOVE_DIVIDERS
    rib_height = top_z - rib_bottom_z
    row_ribs = [
        Pos(LID_SKIRT_OUTER_INSET, y + (DIVIDER_THICKNESS - LID_RIB_THICKNESS) / 2, rib_bottom_z)
        * Box(width - 2 * LID_SKIRT_OUTER_INSET, LID_RIB_THICKNESS, rib_height, align=Align.MIN)
        for y in layout.row_dividers_y
    ]
    column_ribs = [
        Pos(x + (DIVIDER_THICKNESS - LID_RIB_THICKNESS) / 2, layout.pen_divider_y, rib_bottom_z)
        * Box(LID_RIB_THICKNESS, length - LID_SKIRT_OUTER_INSET - layout.pen_divider_y, rib_height, align=Align.MIN)
        for x in layout.column_dividers_x
    ]
    label_y = sum(layout.rows[0]) / 2
    labels = [
        Pos(sum(column) / 2, label_y, top_z + LID_PLATE_THICKNESS) * extrude(Text(size, LABEL_FONT_SIZE), -LABEL_DEPTH)
        for (size, _), column in zip(THREAD_SIZE_COLUMNS, layout.columns, strict=True)
    ]
    lid = plate + skirt + row_ribs + column_ribs + _latches(width, length, rim_z, LATCH_RADIUS, LATCH_LENGTH) - labels
    lid = _lid_flip(length, rim_z) * lid
    lid.label = f"hardware_box_lid_{units_x}x{units_y}x{height_units}"
    return lid
