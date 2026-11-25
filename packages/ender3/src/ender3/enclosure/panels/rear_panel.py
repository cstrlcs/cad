from build123d import Part

from ender3.construction import block
from ender3.enclosure.dimensions import (
    CASE_OUTER_HALF_WIDTH,
    CLEAR_PANEL_BOTTOM_Z,
    CLEAR_PANEL_SIZE,
    REAR_PANEL_Y_RANGE,
)
from ender3.enclosure.panels.construction import acrylic_panel, bracket_holes
from ender3.enclosure.panels.dimensions import CLEAR_ACRYLIC_COLOR


def rear_panel() -> Part:
    panel = block(
        (-CASE_OUTER_HALF_WIDTH, CASE_OUTER_HALF_WIDTH),
        REAR_PANEL_Y_RANGE,
        (CLEAR_PANEL_BOTTOM_Z, CLEAR_PANEL_BOTTOM_Z + CLEAR_PANEL_SIZE),
    )
    panel -= bracket_holes("rear_panel")
    return acrylic_panel(panel, "rear_panel", CLEAR_ACRYLIC_COLOR)
