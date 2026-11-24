from build123d import Part, Polygon, extrude

from ender3_cad.ender3.reference.profiles.construction import mirrored_quadrants, vslot_section
from ender3_cad.ender3.reference.profiles.dimensions import (
    INNER_POCKET_HALF_WIDTH,
    SLOT_BOTTOM_HALF_WIDTH,
    SLOT_CAVITY_HALF_WIDTH,
    SLOT_DEPTH,
    SLOT_GROOVE_HALF_WIDTH,
    SLOT_UNDERCUT_DEPTH,
)

VSLOT_2040_VOID_QUADRANT = [
    (INNER_POCKET_HALF_WIDTH, SLOT_UNDERCUT_DEPTH),
    (SLOT_CAVITY_HALF_WIDTH, SLOT_UNDERCUT_DEPTH),
    (SLOT_BOTTOM_HALF_WIDTH, SLOT_DEPTH),
    (SLOT_GROOVE_HALF_WIDTH, SLOT_DEPTH),
    (0.0, SLOT_DEPTH + SLOT_GROOVE_HALF_WIDTH),
]


def vslot_2040(length: float) -> Part:
    void = Polygon(*mirrored_quadrants(VSLOT_2040_VOID_QUADRANT))
    return extrude(vslot_section(1, 2, [void]), amount=length)
