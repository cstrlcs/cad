from build123d import Polygon, Pos, Rectangle, Rot, Sketch

from ender3_cad.dimensions import CUT_OVERSHOOT
from ender3_cad.ender3.reference.construction import circles
from ender3_cad.ender3.reference.profiles.dimensions import (
    CELL_SIZE,
    CENTER_BORE_DIAMETER,
    SLOT_BOTTOM_HALF_WIDTH,
    SLOT_CAVITY_HALF_WIDTH,
    SLOT_DEPTH,
    SLOT_GROOVE_HALF_WIDTH,
    SLOT_LIP_HALF_GAP,
    SLOT_LIP_THICKNESS,
    SLOT_OPENING_HALF_WIDTH,
    SLOT_UNDERCUT_DEPTH,
)

SLOT_HALF_OUTLINE = [
    (SLOT_OPENING_HALF_WIDTH + CUT_OVERSHOOT, CUT_OVERSHOOT),
    (SLOT_LIP_HALF_GAP, -SLOT_LIP_THICKNESS),
    (SLOT_CAVITY_HALF_WIDTH, -SLOT_LIP_THICKNESS),
    (SLOT_CAVITY_HALF_WIDTH, -SLOT_UNDERCUT_DEPTH),
    (SLOT_BOTTOM_HALF_WIDTH, -SLOT_DEPTH),
    (SLOT_GROOVE_HALF_WIDTH, -SLOT_DEPTH),
    (0.0, -SLOT_DEPTH - SLOT_GROOVE_HALF_WIDTH),
]


def mirrored_halves(half: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return half + [(-x, y) for x, y in reversed(half) if x != 0]


def mirrored_quadrants(quadrant: list[tuple[float, float]]) -> list[tuple[float, float]]:
    upper = mirrored_halves(quadrant)
    return upper + [(x, -y) for x, y in reversed(upper) if y != 0]


SLOT_OUTLINE = mirrored_halves(SLOT_HALF_OUTLINE)


def vslot_section(cells_x: int, cells_y: int, voids: list[Sketch]) -> Sketch:
    width, height = cells_x * CELL_SIZE, cells_y * CELL_SIZE
    cell_offsets_x = [(i - (cells_x - 1) / 2) * CELL_SIZE for i in range(cells_x)]
    cell_offsets_y = [(j - (cells_y - 1) / 2) * CELL_SIZE for j in range(cells_y)]
    slot = Polygon(*SLOT_OUTLINE)
    slots = (
        [Pos(x, height / 2) * slot for x in cell_offsets_x]
        + [Pos(x, -height / 2) * Rot(0, 0, 180) * slot for x in cell_offsets_x]
        + [Pos(width / 2, y) * Rot(0, 0, -90) * slot for y in cell_offsets_y]
        + [Pos(-width / 2, y) * Rot(0, 0, 90) * slot for y in cell_offsets_y]
    )
    bores = circles([(x, y) for x in cell_offsets_x for y in cell_offsets_y], CENTER_BORE_DIAMETER)
    return Rectangle(width, height) - slots - bores - voids
