from build123d import Part

from ender3_cad.construction import block
from ender3_cad.enclosure.dimensions import (
    CASE_INNER_TOP_Z,
    CASE_OUTER_HALF_WIDTH,
    CLEAR_ACRYLIC_THICKNESS,
    DOOR_BACK_Y,
    REAR_PANEL_FRONT_Y,
)
from ender3_cad.enclosure.panels.construction import acrylic_panel, bracket_holes
from ender3_cad.enclosure.panels.dimensions import CLEAR_ACRYLIC_COLOR


def top_panel() -> Part:
    panel = block(
        (-CASE_OUTER_HALF_WIDTH, CASE_OUTER_HALF_WIDTH),
        (DOOR_BACK_Y, REAR_PANEL_FRONT_Y),
        (CASE_INNER_TOP_Z, CASE_INNER_TOP_Z + CLEAR_ACRYLIC_THICKNESS),
    )
    return acrylic_panel(panel - bracket_holes("top_panel"), "top_panel", CLEAR_ACRYLIC_COLOR)
