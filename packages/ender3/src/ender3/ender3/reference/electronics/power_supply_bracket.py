from build123d import Axis, Part, Plane, Polygon, Pos, Rot, SlotCenterToCenter, extrude, fillet

from ender3.construction import block
from ender3.dimensions import CUT_OVERSHOOT, FACE_BACK, FACE_RIGHT
from ender3.ender3.reference.construction import outline_face
from ender3.ender3.reference.electronics.construction import thin_plate_hole

POWER_SUPPLY_BRACKET_LOCATION = Pos(120.5, 0, 57.5)
POWER_SUPPLY_BRACKET_WIDTH = 54.0
POWER_SUPPLY_BRACKET_DEPTH = 115.0
POWER_SUPPLY_BRACKET_HEIGHT = 70.0
POWER_SUPPLY_BRACKET_THICKNESS = 2.0
POWER_SUPPLY_BRACKET_FRONT_BEND_RADIUS = 10.0
POWER_SUPPLY_BRACKET_OPENING_X_RANGE = (2.0, 32.5)
POWER_SUPPLY_BRACKET_FRONT_LIP_HEIGHT = 29.0
POWER_SUPPLY_BRACKET_CABLE_SLOT_CENTER_X = 20.0
POWER_SUPPLY_BRACKET_CABLE_SLOT_CENTERS_Y = (62.0, 74.0)
POWER_SUPPLY_BRACKET_CABLE_SLOT_WIDTH = 16.0
POWER_SUPPLY_BRACKET_BACK_HOLE_DIAMETER = 4.5
POWER_SUPPLY_BRACKET_BACK_HOLE = (13.5, 62.0)
POWER_SUPPLY_BRACKET_SWITCH_BOSS_OUTLINE = [
    (20.5, 14.0),
    (49.5, 14.0 - 29.0 * 11.0 / 30.0),
    (78.5, 14.0),
    (78.5, 42.0),
    (49.5, 42.0 + 29.0 * 11.0 / 30.0),
    (20.5, 42.0),
]
POWER_SUPPLY_BRACKET_SWITCH_BOSS_HEIGHT = 2.0
POWER_SUPPLY_BRACKET_SWITCH_BOSS_EDGE_RADIUS = 1.0
POWER_SUPPLY_BRACKET_SWITCH_BOSS_CORNER_RADIUS = 3.0
POWER_SUPPLY_BRACKET_SWITCH_CUTOUT_Y_RANGE = (25.0, 74.0)
POWER_SUPPLY_BRACKET_SWITCH_CUTOUT_Z_RANGE = (14.0, 42.0)
POWER_SUPPLY_BRACKET_SWITCH_SCREW_HOLE_DIAMETER = 2.6
POWER_SUPPLY_BRACKET_SWITCH_SCREW_HOLES = [(49.5, 8.0), (49.5, 48.0)]


def power_supply_bracket() -> Part:
    t = POWER_SUPPLY_BRACKET_THICKNESS
    width, depth, height = POWER_SUPPLY_BRACKET_WIDTH, POWER_SUPPLY_BRACKET_DEPTH, POWER_SUPPLY_BRACKET_HEIGHT
    radius = POWER_SUPPLY_BRACKET_FRONT_BEND_RADIUS
    outer = outline_face([(0, 0), (depth, 0), (depth, height), (0, height)], [0, 0, 0, radius])
    inner = outline_face(
        [(t, t), (depth - t, t), (depth - t, height - t), (t, height - t)],
        [0, 0, 0, radius - t],
    )
    bracket = extrude(Plane.YZ * outer, width) - extrude(Plane.YZ.offset(t) * inner, width - 2 * t)
    opening = block(
        POWER_SUPPLY_BRACKET_OPENING_X_RANGE,
        (-CUT_OVERSHOOT, depth - t),
        (POWER_SUPPLY_BRACKET_FRONT_LIP_HEIGHT, height + CUT_OVERSHOOT),
    )
    slot_start, slot_end = POWER_SUPPLY_BRACKET_CABLE_SLOT_CENTERS_Y
    cable_slot = Pos(POWER_SUPPLY_BRACKET_CABLE_SLOT_CENTER_X, (slot_start + slot_end) / 2, -CUT_OVERSHOOT) * extrude(
        Rot(0, 0, 90) * SlotCenterToCenter(slot_end - slot_start, POWER_SUPPLY_BRACKET_CABLE_SLOT_WIDTH),
        t + 2 * CUT_OVERSHOOT,
    )
    hole_x, hole_z = POWER_SUPPLY_BRACKET_BACK_HOLE
    back_hole = Pos(hole_x, depth, hole_z) * FACE_BACK * thin_plate_hole(POWER_SUPPLY_BRACKET_BACK_HOLE_DIAMETER)
    boss_height = POWER_SUPPLY_BRACKET_SWITCH_BOSS_HEIGHT
    boss_outline = Polygon(*POWER_SUPPLY_BRACKET_SWITCH_BOSS_OUTLINE, align=None)
    boss_outline = fillet(boss_outline.vertices(), POWER_SUPPLY_BRACKET_SWITCH_BOSS_CORNER_RADIUS)
    switch_boss = extrude(Plane.YZ.offset(width) * boss_outline, boss_height)
    switch_cutout = block(
        (width - t - CUT_OVERSHOOT, width + boss_height + CUT_OVERSHOOT),
        POWER_SUPPLY_BRACKET_SWITCH_CUTOUT_Y_RANGE,
        POWER_SUPPLY_BRACKET_SWITCH_CUTOUT_Z_RANGE,
    )
    switch_screw_holes = [
        Pos(width, y, z) * FACE_RIGHT * thin_plate_hole(POWER_SUPPLY_BRACKET_SWITCH_SCREW_HOLE_DIAMETER)
        for y, z in POWER_SUPPLY_BRACKET_SWITCH_SCREW_HOLES
    ]
    switch_boss = fillet(switch_boss.edges().group_by(Axis.X)[-1], POWER_SUPPLY_BRACKET_SWITCH_BOSS_EDGE_RADIUS)
    bracket = bracket - opening - cable_slot - back_hole + switch_boss - switch_cutout - switch_screw_holes
    bracket = POWER_SUPPLY_BRACKET_LOCATION * bracket
    bracket.label = "power_supply_bracket"
    return bracket
