from build123d import Part, Vector

from ender3_cad.construction import block
from ender3_cad.dimensions import M3_CLEARANCE_DIAMETER
from ender3_cad.enclosure.construction import frame_hinge_screw_points, hole, switch_cavity_ranges, switch_screw_points
from ender3_cad.enclosure.dimensions import CASE_INNER_HALF_WIDTH, CASE_OUTER_HALF_WIDTH, HINGE_CENTERS_Z
from ender3_cad.enclosure.panels.construction import side_panel
from ender3_cad.ender3.reference.electronics.dimensions import POWER_SWITCH_SCREW_HOLE_DIAMETER

SWITCH_WINDOW_OVERSHOOT = 1.0


def left_side_panel() -> Part:
    _, cavity_y, cavity_z = switch_cavity_ranges()
    hinge_holes = [
        hole(point, Vector(1, 0, 0), M3_CLEARANCE_DIAMETER)
        for center_z in HINGE_CENTERS_Z
        for point in frame_hinge_screw_points(center_z)
    ]
    switch_window = block(
        (-CASE_OUTER_HALF_WIDTH - SWITCH_WINDOW_OVERSHOOT, -CASE_INNER_HALF_WIDTH + SWITCH_WINDOW_OVERSHOOT),
        cavity_y,
        cavity_z,
    )
    switch_holes = [hole(point, Vector(1, 0, 0), POWER_SWITCH_SCREW_HOLE_DIAMETER) for point in switch_screw_points()]
    return side_panel(-1, [*hinge_holes, switch_window, *switch_holes])
