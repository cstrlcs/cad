from build123d import Axis, Cone, Part, Plane, Polygon, Pos, chamfer, extrude, offset

from ender3.construction import block
from ender3.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_RIGHT
from ender3.ender3.reference.electronics.construction import thin_plate_hole
from ender3.ender3.reference.electronics.dimensions import (
    POWER_SWITCH_BODY_Y,
    POWER_SWITCH_BODY_Z,
    POWER_SWITCH_FLANGE_CORNER_CENTERS,
    POWER_SWITCH_FLANGE_CORNER_RADIUS,
    POWER_SWITCH_LOCATION,
    POWER_SWITCH_SCREW_HOLE_DIAMETER,
    POWER_SWITCH_SCREW_HOLES,
    POWER_SWITCH_SOLDER_TAB_X,
)

POWER_SWITCH_FLANGE_THICKNESS = 4.0

POWER_SWITCH_SCREW_COUNTERSINK_DIAMETER = 6.5

POWER_SWITCH_BODY_X_RANGE = (-18.2, 0.0)

POWER_SWITCH_BODY_CHAMFER = 3.0
POWER_SWITCH_INLET_FLOOR_X = -6.0
POWER_SWITCH_INLET_OUTLINE = [
    (6.877, -12.15),
    (19.001, -12.15),
    (23.377, -8.755),
    (23.377, 8.755),
    (19.001, 12.15),
    (6.877, 12.15),
]
POWER_SWITCH_INLET_PIN_X_RANGE = (-6.0, 2.0)
POWER_SWITCH_INLET_PINS = [
    ((17.12, 19.843), (-0.835, -0.013)),
    ((12.227, 15.79), (4.646, 5.39)),
    ((12.249, 15.079), (-4.897, -4.284)),
]
POWER_SWITCH_ROCKER_Y_RANGE = (-16.65, -10.65)
POWER_SWITCH_ROCKER_PROFILE = [(4.0, -7.938), (4.687, -7.708), (9.446, 9.312), (9.254, 9.566), (4.0, 9.566)]

POWER_SWITCH_SOLDER_TABS = [
    ((-1.797, -1.129), (-8.111, -4.774)),
    ((9.445, 10.113), (-8.111, -4.774)),
    ((17.042, 17.915), (-1.489, 2.567)),
    ((-15.656, -11.755), (3.747, 4.723)),
    ((-15.656, -11.755), (-2.259, -1.489)),
    ((-15.656, -11.755), (-6.673, -5.903)),
]


def power_switch() -> Part:
    flange_outline = offset(Polygon(*POWER_SWITCH_FLANGE_CORNER_CENTERS, align=None), POWER_SWITCH_FLANGE_CORNER_RADIUS)
    flange = extrude(Plane.YZ * flange_outline, POWER_SWITCH_FLANGE_THICKNESS)
    hole_radius = POWER_SWITCH_SCREW_HOLE_DIAMETER / 2
    countersink_radius = POWER_SWITCH_SCREW_COUNTERSINK_DIAMETER / 2
    countersink_depth = countersink_radius - hole_radius
    screw_holes = [
        Pos(0, y, z) * FACE_RIGHT * thin_plate_hole(POWER_SWITCH_SCREW_HOLE_DIAMETER)
        + Pos(POWER_SWITCH_FLANGE_THICKNESS - countersink_depth, y, z)
        * FACE_RIGHT
        * Cone(hole_radius, countersink_radius + CUT_OVERSHOOT, countersink_depth + CUT_OVERSHOOT, align=BOTTOM)
        for y, z in POWER_SWITCH_SCREW_HOLES
    ]
    body = block(POWER_SWITCH_BODY_X_RANGE, POWER_SWITCH_BODY_Y, POWER_SWITCH_BODY_Z)
    body = chamfer(body.edges().filter_by(Axis.X).group_by(Axis.Y)[-1], POWER_SWITCH_BODY_CHAMFER)
    inlet = extrude(
        Plane.YZ.offset(POWER_SWITCH_INLET_FLOOR_X) * Polygon(*POWER_SWITCH_INLET_OUTLINE, align=None),
        POWER_SWITCH_FLANGE_THICKNESS - POWER_SWITCH_INLET_FLOOR_X + CUT_OVERSHOOT,
    )
    inlet_pins = [
        block(POWER_SWITCH_INLET_PIN_X_RANGE, y_range, z_range) for y_range, z_range in POWER_SWITCH_INLET_PINS
    ]
    rocker_y0, rocker_y1 = POWER_SWITCH_ROCKER_Y_RANGE
    rocker = extrude(
        Plane.XZ.offset(-rocker_y0) * Polygon(*POWER_SWITCH_ROCKER_PROFILE, align=None), -(rocker_y1 - rocker_y0)
    )
    solder_tabs = [block(POWER_SWITCH_SOLDER_TAB_X, y_range, z_range) for y_range, z_range in POWER_SWITCH_SOLDER_TABS]
    switch = flange + body - screw_holes - inlet + inlet_pins + rocker + solder_tabs
    switch = POWER_SWITCH_LOCATION * switch
    switch.label = "power_switch"
    return switch
