from build123d import Align, Box, Circle, Cylinder, Part, Plane, Pos, Rectangle, extrude

from ender3.dimensions import BOTTOM, FACE_BACK, FACE_FRONT
from ender3.ender3.reference.construction import circles, outline_face
from ender3.ender3.reference.print_head.dimensions import (
    X_CARRIAGE_PLATE_CENTER_HOLE,
    X_CARRIAGE_PLATE_FAN_COVER_BOSS_HEIGHT,
    X_CARRIAGE_PLATE_FAN_COVER_HOLES,
    X_CARRIAGE_PLATE_HOTEND_STANDOFF_HEIGHT,
    X_CARRIAGE_PLATE_HOTEND_STANDOFFS,
    X_CARRIAGE_PLATE_LOCATION,
    X_CARRIAGE_PLATE_THICKNESS,
    X_CARRIAGE_PLATE_UPPER_HOLES,
)

X_CARRIAGE_PLATE_WIDTH = 64.0
X_CARRIAGE_PLATE_HEIGHT = 47.5

X_CARRIAGE_PLATE_CORNER_RADIUS = 10.0
X_CARRIAGE_PLATE_LOBE_WIDTH = 24.0
X_CARRIAGE_PLATE_LOBE_CENTER = (0.0, -4.5)

X_CARRIAGE_PLATE_CENTER_HOLE_DIAMETER = 7.2

X_CARRIAGE_PLATE_UPPER_HOLE_DIAMETER = 5.0

X_CARRIAGE_PLATE_FAN_COVER_HOLE_DIAMETER = 3.0
X_CARRIAGE_PLATE_FAN_COVER_BOSS_DIAMETER = 4.0

X_CARRIAGE_PLATE_HOTEND_STANDOFF_DIAMETER = 5.4

X_CARRIAGE_PLATE_HOTEND_STANDOFF_HOLE_DIAMETER = 3.0
X_CARRIAGE_PLATE_TAB_DEPTH = 22.9
X_CARRIAGE_PLATE_TAB_X_RANGES = [(-32.0, -15.0), (15.0, 32.0)]
X_CARRIAGE_PLATE_TAB_CORNER_RADIUS = 2.0
X_CARRIAGE_PLATE_TAB_SLOT_X_RANGES = [(-21.5, -20.0), (20.0, 21.5)]
X_CARRIAGE_PLATE_TAB_SLOT_DEPTH = 11.0


def x_carriage_plate() -> Part:
    half_width = X_CARRIAGE_PLATE_WIDTH / 2
    lobe_radius = X_CARRIAGE_PLATE_LOBE_WIDTH / 2
    lobe_x, lobe_z = X_CARRIAGE_PLATE_LOBE_CENTER
    outline = outline_face(
        [
            (-half_width, 0),
            (half_width, 0),
            (half_width, X_CARRIAGE_PLATE_HEIGHT),
            (-half_width, X_CARRIAGE_PLATE_HEIGHT),
        ],
        [0, 0, X_CARRIAGE_PLATE_CORNER_RADIUS, X_CARRIAGE_PLATE_CORNER_RADIUS],
    )
    lobe = Pos(lobe_x, lobe_z) * (
        Circle(lobe_radius) + Rectangle(X_CARRIAGE_PLATE_LOBE_WIDTH, -2 * lobe_z, align=(Align.CENTER, Align.MIN))
    )
    holes = (
        circles([X_CARRIAGE_PLATE_CENTER_HOLE], X_CARRIAGE_PLATE_CENTER_HOLE_DIAMETER)
        + circles(X_CARRIAGE_PLATE_UPPER_HOLES, X_CARRIAGE_PLATE_UPPER_HOLE_DIAMETER)
        + circles(X_CARRIAGE_PLATE_FAN_COVER_HOLES, X_CARRIAGE_PLATE_FAN_COVER_HOLE_DIAMETER)
        + circles(X_CARRIAGE_PLATE_HOTEND_STANDOFFS, X_CARRIAGE_PLATE_HOTEND_STANDOFF_HOLE_DIAMETER)
    )
    plate = extrude(Plane.XZ * (outline + lobe - holes), -X_CARRIAGE_PLATE_THICKNESS)
    for x_start, x_end in X_CARRIAGE_PLATE_TAB_X_RANGES:
        tab_outline = outline_face(
            [
                (x_start, 0),
                (x_end, 0),
                (x_end, X_CARRIAGE_PLATE_TAB_DEPTH),
                (x_start, X_CARRIAGE_PLATE_TAB_DEPTH),
            ],
            [0, 0, X_CARRIAGE_PLATE_TAB_CORNER_RADIUS, X_CARRIAGE_PLATE_TAB_CORNER_RADIUS],
        )
        plate += extrude(tab_outline, X_CARRIAGE_PLATE_THICKNESS)
    for x_start, x_end in X_CARRIAGE_PLATE_TAB_SLOT_X_RANGES:
        plate -= Pos(x_start, X_CARRIAGE_PLATE_TAB_DEPTH - X_CARRIAGE_PLATE_TAB_SLOT_DEPTH, 0) * Box(
            x_end - x_start,
            X_CARRIAGE_PLATE_TAB_SLOT_DEPTH,
            X_CARRIAGE_PLATE_THICKNESS,
            align=Align.MIN,
        )
    for x, z in X_CARRIAGE_PLATE_FAN_COVER_HOLES:
        boss = Cylinder(
            X_CARRIAGE_PLATE_FAN_COVER_BOSS_DIAMETER / 2,
            X_CARRIAGE_PLATE_FAN_COVER_BOSS_HEIGHT,
            align=BOTTOM,
        )
        hole = Cylinder(
            X_CARRIAGE_PLATE_FAN_COVER_HOLE_DIAMETER / 2,
            X_CARRIAGE_PLATE_FAN_COVER_BOSS_HEIGHT,
            align=BOTTOM,
        )
        plate += Pos(x, X_CARRIAGE_PLATE_THICKNESS, z) * FACE_BACK * (boss - hole)
    for x, z in X_CARRIAGE_PLATE_HOTEND_STANDOFFS:
        standoff = Cylinder(
            X_CARRIAGE_PLATE_HOTEND_STANDOFF_DIAMETER / 2,
            X_CARRIAGE_PLATE_HOTEND_STANDOFF_HEIGHT,
            align=BOTTOM,
        )
        hole = Cylinder(
            X_CARRIAGE_PLATE_HOTEND_STANDOFF_HOLE_DIAMETER / 2,
            X_CARRIAGE_PLATE_HOTEND_STANDOFF_HEIGHT,
            align=BOTTOM,
        )
        plate += Pos(x, 0, z) * FACE_FRONT * (standoff - hole)
    plate = X_CARRIAGE_PLATE_LOCATION * plate
    plate.label = "x_carriage_plate"
    return plate
