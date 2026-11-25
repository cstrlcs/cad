from math import sqrt

from build123d import Cylinder, Part, Plane, Polygon, Pos, extrude

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block
from ender3.dimensions import BOTTOM, FACE_BACK, M5_CLEARANCE_DIAMETER
from ender3.enclosure.dimensions import DOOR_FRONT_Y, DRAWER_FRONT_INNER_X
from ender3.upgrades.board_cases.dimensions import (
    CEILING_BOTTOM_Z,
    CEILING_TOP_Z,
    LEFT_PANEL_OUTER_X,
    LEFT_PANEL_SCREW_HOLES,
    PANEL_FRONT_Y,
    TRAY_BOTTOM_Z,
    WALL_THICKNESS,
)

DRAWER_FRONT_THICKNESS = 4.0
DRAWER_FRONT_BACK_PLATE_THICKNESS = 4.0

STORAGE_CAVITY_X = (LEFT_PANEL_OUTER_X + WALL_THICKNESS, DRAWER_FRONT_INNER_X - WALL_THICKNESS)
STORAGE_LEDGE_WIDTH = 3.0
STORAGE_CLEARANCE = 0.3
STORAGE_BOTTOM_LIFT = 0.4
STORAGE_WALL = 2.0
STORAGE_FLOOR = 3.0
STORAGE_TOP_GAP = 1.0
STORAGE_BACK_GAP = 1.0
STORAGE_PULL_WIDTH = 40.0
STORAGE_PULL_DEPTH = 12.0


def left_storage_housing_body() -> Part:
    front_y = DOOR_FRONT_Y + DRAWER_FRONT_THICKNESS
    housing = block(
        (LEFT_PANEL_OUTER_X, DRAWER_FRONT_INNER_X), (front_y, PANEL_FRONT_Y), (TRAY_BOTTOM_Z, CEILING_TOP_Z)
    )
    housing -= block(
        STORAGE_CAVITY_X,
        (front_y, PANEL_FRONT_Y - DRAWER_FRONT_BACK_PLATE_THICKNESS),
        (TRAY_BOTTOM_Z, CEILING_BOTTOM_Z),
    )
    for wall_x, inward in ((STORAGE_CAVITY_X[0], 1), (STORAGE_CAVITY_X[1], -1)):
        ledge = Polygon(
            (wall_x, TRAY_BOTTOM_Z),
            (wall_x + inward * STORAGE_LEDGE_WIDTH, TRAY_BOTTOM_Z),
            (wall_x, TRAY_BOTTOM_Z + STORAGE_LEDGE_WIDTH),
            align=None,
        )
        ledge_length = PANEL_FRONT_Y - DRAWER_FRONT_BACK_PLATE_THICKNESS - front_y
        housing += Pos(0, front_y, 0) * extrude(Plane.XZ * ledge, ledge_length, dir=(0, 1, 0))
    housing -= [
        Pos(x, PANEL_FRONT_Y - DRAWER_FRONT_BACK_PLATE_THICKNESS, z)
        * FACE_BACK
        * Cylinder(M5_CLEARANCE_DIAMETER / 2, DRAWER_FRONT_BACK_PLATE_THICKNESS, align=BOTTOM)
        for x, z in LEFT_PANEL_SCREW_HOLES
    ]
    return housing


def left_storage_drawer_body() -> Part:
    x0, x1 = STORAGE_CAVITY_X[0] + STORAGE_CLEARANCE, STORAGE_CAVITY_X[1] - STORAGE_CLEARANCE
    bottom_z = TRAY_BOTTOM_Z + STORAGE_BOTTOM_LIFT
    chamfer_rise = STORAGE_LEDGE_WIDTH + STORAGE_CLEARANCE * sqrt(2) - STORAGE_CLEARANCE
    chamfer_run = STORAGE_LEDGE_WIDTH + STORAGE_CLEARANCE * sqrt(2) - STORAGE_BOTTOM_LIFT
    corner_z = TRAY_BOTTOM_Z + chamfer_rise
    top_z = CEILING_BOTTOM_Z - STORAGE_TOP_GAP
    back_y = PANEL_FRONT_Y - DRAWER_FRONT_BACK_PLATE_THICKNESS - STORAGE_BACK_GAP
    plate_back_y = DOOR_FRONT_Y + DRAWER_FRONT_THICKNESS
    profile = Polygon(
        (x0, top_z),
        (x0, corner_z),
        (STORAGE_CAVITY_X[0] + chamfer_run, bottom_z),
        (STORAGE_CAVITY_X[1] - chamfer_run, bottom_z),
        (x1, corner_z),
        (x1, top_z),
        align=None,
    )
    box = Pos(0, plate_back_y, 0) * extrude(Plane.XZ * profile, back_y - plate_back_y, dir=(0, 1, 0))
    box -= block(
        (x0 + STORAGE_WALL, x1 - STORAGE_WALL),
        (plate_back_y, back_y - STORAGE_WALL),
        (bottom_z + STORAGE_FLOOR, top_z),
    )
    front = block(
        (LEFT_PANEL_OUTER_X, DRAWER_FRONT_INNER_X),
        (DOOR_FRONT_Y, plate_back_y),
        (TRAY_BOTTOM_Z, CEILING_TOP_Z - STORAGE_TOP_GAP),
    )
    pull_x = (LEFT_PANEL_OUTER_X + DRAWER_FRONT_INNER_X) / 2
    front -= block(
        (pull_x - STORAGE_PULL_WIDTH / 2, pull_x + STORAGE_PULL_WIDTH / 2),
        (DOOR_FRONT_Y, plate_back_y),
        (CEILING_TOP_Z - STORAGE_TOP_GAP - STORAGE_PULL_DEPTH, CEILING_TOP_Z),
    )
    return box + front


def labelled(part: Part, label: str) -> Part:
    part.label = label
    part.color = PRINTED_PART_COLOR
    return part
