from build123d import Part, Vector

from ender3.construction import block
from ender3.dimensions import M3_CLEARANCE_DIAMETER
from ender3.enclosure.construction import (
    door_hinge_screw_points,
    handle_screw_points,
    hole,
    latch_holder_screw_point,
)
from ender3.enclosure.dimensions import (
    CASE_OUTER_HALF_WIDTH,
    CLEAR_PANEL_SIZE,
    DOOR_BACK_Y,
    DOOR_BOTTOM_Z,
    DOOR_FRONT_Y,
    HINGE_CENTERS_Z,
)
from ender3.enclosure.panels.construction import acrylic_panel
from ender3.enclosure.panels.dimensions import CLEAR_ACRYLIC_COLOR


def front_door() -> Part:
    door = block(
        (-CASE_OUTER_HALF_WIDTH, CASE_OUTER_HALF_WIDTH),
        (DOOR_FRONT_Y, DOOR_BACK_Y),
        (DOOR_BOTTOM_Z, DOOR_BOTTOM_Z + CLEAR_PANEL_SIZE),
    )
    screw_points = [
        *(point for center_z in HINGE_CENTERS_Z for point in door_hinge_screw_points(center_z)),
        latch_holder_screw_point(),
        *handle_screw_points(),
    ]
    door -= [hole(point, Vector(0, 1, 0), M3_CLEARANCE_DIAMETER) for point in screw_points]
    return acrylic_panel(door, "front_door", CLEAR_ACRYLIC_COLOR)
