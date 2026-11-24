from build123d import Cylinder, Part, Pos, Rot, Vector

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import BOTTOM, M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3_cad.enclosure.construction import blind_hole, switch_cavity_ranges, switch_screw_points
from ender3_cad.enclosure.dimensions import CLEAR_PANEL_BOTTOM_Z, SWITCH_CENTER_Y

SWITCH_HOUSING_WALL = 2.5
SWITCH_HOUSING_SCREW_MARGIN = 4.0
SWITCH_WIRE_HOLE_DIAMETER = 10.0
SWITCH_WIRE_HOLE_INSET = 8.0
SWITCH_WIRE_HOLE_OVERSHOOT = 1.0


def _switch_wire_hole_center() -> Vector:
    cavity_x, _, _ = switch_cavity_ranges()
    return Vector(cavity_x[1] - SWITCH_WIRE_HOLE_INSET, SWITCH_CENTER_Y, CLEAR_PANEL_BOTTOM_Z)


def power_switch_housing() -> Part:
    cavity_x, cavity_y, cavity_z = switch_cavity_ranges()
    wall = SWITCH_HOUSING_WALL
    top_z = max(point.Z for point in switch_screw_points()) + SWITCH_HOUSING_SCREW_MARGIN
    housing = block(
        (cavity_x[0], cavity_x[1] + wall), (cavity_y[0] - wall, cavity_y[1] + wall), (CLEAR_PANEL_BOTTOM_Z, top_z)
    )
    housing -= block(cavity_x, cavity_y, cavity_z)
    wire = _switch_wire_hole_center()
    housing -= Pos(wire.X, wire.Y, wire.Z) * Cylinder(
        SWITCH_WIRE_HOLE_DIAMETER / 2, cavity_z[0] - wire.Z + SWITCH_WIRE_HOLE_OVERSHOOT, align=BOTTOM
    )
    housing -= [
        blind_hole(
            Vector(cavity_x[0], p.Y, p.Z), Vector(1, 0, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
        )
        for p in switch_screw_points()
    ]
    housing.label = "power_switch_housing"
    housing.color = PRINTED_PART_COLOR
    return housing


def power_switch_housing_for_printing() -> Part:
    return resting_on_bed(Rot(0, -90, 0) * power_switch_housing())
