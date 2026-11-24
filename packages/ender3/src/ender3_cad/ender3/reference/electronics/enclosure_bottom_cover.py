from math import cos, radians, sin

from build123d import Align, Circle, Part, Plane, Pos, Rectangle, Rot, Sketch, SlotCenterToCenter, extrude

from ender3_cad.dimensions import CUT_OVERSHOOT
from ender3_cad.ender3.reference.construction import outline_face
from ender3_cad.ender3.reference.electronics.construction import thin_plate_hole
from ender3_cad.ender3.reference.electronics.dimensions import (
    ENCLOSURE_CORNER_RADIUS,
    ENCLOSURE_LOCATION,
    ENCLOSURE_SCREW_HOLE_DIAMETER,
    ENCLOSURE_SHEET_THICKNESS,
)

BOTTOM_COVER_LENGTH = 164.0
BOTTOM_COVER_FLAT_WIDTH = 102.5
BOTTOM_COVER_WIDTH = 104.0
BOTTOM_COVER_HEIGHT = 40.0
BOTTOM_COVER_BEND_INNER_RADIUS = 0.5
BOTTOM_COVER_WALL_LENGTH = 110.0
BOTTOM_COVER_TOP_FLANGE_INNER_EDGE_X = 94.0
BOTTOM_COVER_BASE_SCREW_HOLES = [(9.0, 4.0), (95.0, 4.0), (65.0, 134.0)]
BOTTOM_COVER_TOP_FLANGE_SCREW_HOLE = (99.0, 55.0)

FAN_GRILLE_CENTER = (28.5, 60.5)
FAN_GRILLE_OUTER_DIAMETER = 37.0
FAN_GRILLE_RING_DIAMETERS = [(FAN_GRILLE_OUTER_DIAMETER, 29.0), (23.0, 15.0)]
FAN_GRILLE_CENTER_HOLE_DIAMETER = 9.0
FAN_GRILLE_SPOKE_WIDTH = 3.0

BASE_VENT_SLOT_CENTER_DISTANCE = 20.0
BASE_VENT_SLOT_WIDTH = 3.0
BASE_VENT_SLOT_CENTERS = [(35.5, y) for y in (25.5, 35.5, 85.5, 95.5, 105.5, 115.5, 125.5)] + [
    (76.5, 25.5 + 10.0 * i) for i in range(11)
]
WALL_VENT_SLOT_CENTER_DISTANCE = 20.0
WALL_VENT_SLOT_WIDTH = 3.0
WALL_VENT_SLOT_ANGLE = 45.0
WALL_VENT_SLOT_LOWER_END_CENTERS = [(6.5 + 12.0 * i, 11.5) for i in range(8)]


def _bottom_cover_wall_profile() -> Sketch:
    t = ENCLOSURE_SHEET_THICKNESS
    r = BOTTOM_COVER_BEND_INNER_RADIUS
    bend_x = BOTTOM_COVER_FLAT_WIDTH
    top = BOTTOM_COVER_HEIGHT
    bend = Circle(r + t) - Circle(r)
    quadrant = Rectangle(r + t, r + t, align=Align.MIN)
    lower_bend = Pos(bend_x, r) * (bend & Rot(0, 0, -90) * quadrant)
    upper_bend = Pos(bend_x, top - t - r) * (bend & quadrant)
    wall = Pos(bend_x + r, r) * Rectangle(t, top - t - 2 * r, align=Align.MIN)
    return lower_bend + upper_bend + wall


def enclosure_bottom_cover() -> Part:
    t = ENCLOSURE_SHEET_THICKNESS
    radius = ENCLOSURE_CORNER_RADIUS
    base_outline = outline_face(
        [
            (0, 0),
            (BOTTOM_COVER_FLAT_WIDTH, 0),
            (BOTTOM_COVER_FLAT_WIDTH, BOTTOM_COVER_LENGTH),
            (0, BOTTOM_COVER_LENGTH),
        ],
        [radius, 0, radius, radius],
    )
    base = Pos(0, 0, -t) * extrude(base_outline, t)
    wall = extrude(Plane.XZ * _bottom_cover_wall_profile(), -BOTTOM_COVER_WALL_LENGTH)
    flange_x = BOTTOM_COVER_TOP_FLANGE_INNER_EDGE_X
    flange_outline = outline_face(
        [
            (flange_x, 0),
            (BOTTOM_COVER_FLAT_WIDTH, 0),
            (BOTTOM_COVER_FLAT_WIDTH, BOTTOM_COVER_WALL_LENGTH),
            (flange_x, BOTTOM_COVER_WALL_LENGTH),
        ],
        [radius, 0, 0, radius],
    )
    flange = Pos(0, 0, BOTTOM_COVER_HEIGHT - t) * extrude(flange_outline, t)
    screw_holes = [
        Pos(x, y, 0) * thin_plate_hole(ENCLOSURE_SCREW_HOLE_DIAMETER) for x, y in BOTTOM_COVER_BASE_SCREW_HOLES
    ] + [Pos(*BOTTOM_COVER_TOP_FLANGE_SCREW_HOLE, BOTTOM_COVER_HEIGHT) * thin_plate_hole(ENCLOSURE_SCREW_HOLE_DIAMETER)]
    rings = [Circle(outer / 2) - Circle(inner / 2) for outer, inner in FAN_GRILLE_RING_DIAMETERS]
    spoke_length = 2 * FAN_GRILLE_OUTER_DIAMETER
    spokes = Rectangle(spoke_length, FAN_GRILLE_SPOKE_WIDTH) + Rectangle(FAN_GRILLE_SPOKE_WIDTH, spoke_length)
    grille = Pos(*FAN_GRILLE_CENTER) * (Sketch() + rings - spokes + Circle(FAN_GRILLE_CENTER_HOLE_DIAMETER / 2))
    base_slots = [
        Pos(x, y) * SlotCenterToCenter(BASE_VENT_SLOT_CENTER_DISTANCE, BASE_VENT_SLOT_WIDTH)
        for x, y in BASE_VENT_SLOT_CENTERS
    ]
    base_cutouts = Pos(0, 0, -t - CUT_OVERSHOOT) * extrude(Sketch() + grille + base_slots, t + 2 * CUT_OVERSHOOT)
    half = WALL_VENT_SLOT_CENTER_DISTANCE / 2
    angle = radians(WALL_VENT_SLOT_ANGLE)
    wall_slots = [
        Pos(y + half * cos(angle), z + half * sin(angle))
        * Rot(0, 0, WALL_VENT_SLOT_ANGLE)
        * SlotCenterToCenter(WALL_VENT_SLOT_CENTER_DISTANCE, WALL_VENT_SLOT_WIDTH)
        for y, z in WALL_VENT_SLOT_LOWER_END_CENTERS
    ]
    wall_cutouts = extrude(
        Plane.YZ.offset(BOTTOM_COVER_WIDTH - t - CUT_OVERSHOOT) * (Sketch() + wall_slots), t + 2 * CUT_OVERSHOOT
    )
    cover = base + wall + flange - screw_holes - base_cutouts - wall_cutouts
    cover = ENCLOSURE_LOCATION * cover
    cover.label = "enclosure_bottom_cover"
    return cover
