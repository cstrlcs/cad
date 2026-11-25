from build123d import Color, Cylinder, Part, Pos

from ender3.construction import block
from ender3.dimensions import BOTTOM, M3_CLEARANCE_DIAMETER, M4_CLEARANCE_DIAMETER
from ender3.enclosure.construction import bottom_panel_name, bracket_joints, hole, side_panel_name
from ender3.enclosure.dimensions import (
    BRACKET_HOLE_OFFSET,
    CASE_INNER_HALF_WIDTH,
    CASE_INNER_TOP_Z,
    CASE_OUTER_HALF_WIDTH,
    CENTER_PLATE_TOP_Z,
    DOOR_BACK_Y,
    RAIL_END_Y,
    REAR_PANEL_FRONT_Y,
    SIDE_PANEL_BOTTOM_Z,
)
from ender3.enclosure.panels.dimensions import BLACK_ACRYLIC_COLOR, BLACK_ACRYLIC_THICKNESS, CLEAR_ACRYLIC_COLOR
from ender3.ender3.reference.profiles.dimensions import CELL_HALF_SIZE
from ender3.upgrades.board_cases.dimensions import RAIL_INNER_FACE_X, RAIL_OUTER_FACE_X

CASE_BOTTOM_Z = -BLACK_ACRYLIC_THICKNESS

PANEL_EDGE_GAP = 0.3

DOOR_LEG_INNER_X = RAIL_OUTER_FACE_X + PANEL_EDGE_GAP

CENTER_PLATE_THICKNESS = BLACK_ACRYLIC_THICKNESS

CENTER_PLATE_Z = (CENTER_PLATE_TOP_Z - CENTER_PLATE_THICKNESS, CENTER_PLATE_TOP_Z)

REAR_LEG_INNER_X = RAIL_INNER_FACE_X

CENTER_PLATE_SCREW_X = (-CELL_HALF_SIZE, CELL_HALF_SIZE)


def bracket_holes(panel: str) -> list[Part]:
    holes = []
    for joint in bracket_joints():
        if joint.leg_a_panel == panel:
            holes.append(hole(joint.corner + joint.u * BRACKET_HOLE_OFFSET, joint.v, M3_CLEARANCE_DIAMETER))
        if joint.leg_b_panel == panel:
            holes.append(hole(joint.corner + joint.v * BRACKET_HOLE_OFFSET, joint.u, M3_CLEARANCE_DIAMETER))
    return holes


def acrylic_panel(panel: Part, label: str, color: Color) -> Part:
    panel.label = label
    panel.color = color
    return panel


def side_panel(side: int, cutouts: list[Part]) -> Part:
    x_range = tuple(sorted((side * CASE_INNER_HALF_WIDTH, side * CASE_OUTER_HALF_WIDTH)))
    panel = block(x_range, (DOOR_BACK_Y, REAR_PANEL_FRONT_Y), (SIDE_PANEL_BOTTOM_Z, CASE_INNER_TOP_Z))
    panel -= bracket_holes(side_panel_name(side))
    panel -= cutouts
    return acrylic_panel(panel, side_panel_name(side), CLEAR_ACRYLIC_COLOR)


def bottom_panel(side: int) -> Part:
    z_range = (CASE_BOTTOM_Z, 0.0)
    panel = block(
        tuple(sorted((side * DOOR_LEG_INNER_X, side * CASE_INNER_HALF_WIDTH))), (DOOR_BACK_Y, RAIL_END_Y), z_range
    )
    panel += block(
        tuple(sorted((side * REAR_LEG_INNER_X, side * CASE_INNER_HALF_WIDTH))),
        (RAIL_END_Y, REAR_PANEL_FRONT_Y),
        z_range,
    )
    panel -= bracket_holes(bottom_panel_name(side))
    return acrylic_panel(panel, bottom_panel_name(side), BLACK_ACRYLIC_COLOR)


def center_plate(half_width: float, y_range: tuple[float, float], screw_y: tuple[float, float]) -> Part:
    plate = block((-half_width, half_width), y_range, CENTER_PLATE_Z)
    return plate - [
        Pos(x, y, CENTER_PLATE_Z[0]) * Cylinder(M4_CLEARANCE_DIAMETER / 2, CENTER_PLATE_THICKNESS, align=BOTTOM)
        for x in CENTER_PLATE_SCREW_X
        for y in screw_y
    ]
