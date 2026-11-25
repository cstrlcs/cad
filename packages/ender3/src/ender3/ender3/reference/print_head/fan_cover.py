from build123d import (
    Align,
    Circle,
    Cylinder,
    Part,
    Plane,
    Polyline,
    Pos,
    Rectangle,
    SlotCenterToCenter,
    extrude,
    make_face,
)

from ender3.dimensions import BOTTOM, FACE_BACK
from ender3.ender3.reference.components.dimensions import FAN_4010_MOUNTING_HOLES
from ender3.ender3.reference.construction import circles, outline_face
from ender3.ender3.reference.print_head.dimensions import (
    FAN_COVER_FAN_CENTER_X,
    FAN_COVER_FAN_CENTER_Z,
    FAN_COVER_LOCATION,
    FAN_COVER_SHEET_THICKNESS,
)

FAN_COVER_WIDTH = 48.0
FAN_COVER_HEIGHT = 45.7
FAN_COVER_DEPTH = 42.0
FAN_COVER_RIGHT_WALL_DEPTH = 45.0

FAN_COVER_FAN_OPENING_DIAMETER = 36.0
FAN_COVER_GRILLE_RING_DIAMETERS = (20.0, 24.0)
FAN_COVER_GRILLE_HUB_DIAMETER = 14.0
FAN_COVER_GRILLE_SPOKE_WIDTH = 2.0
FAN_COVER_FAN_STANDOFF_DIAMETER = 5.4
FAN_COVER_FAN_STANDOFF_HOLE_DIAMETER = 3.0
FAN_COVER_FAN_STANDOFF_TOP = 5.0

FAN_COVER_EAR_RADIUS = 7.5
FAN_COVER_EAR_HOLE_DIAMETER = 4.0
FAN_COVER_SIDE_EAR_CENTER = (-25.5, 8.35)
FAN_COVER_SIDE_EAR_HOLE = (-28.0, 8.35)
FAN_COVER_TOP_EAR_CENTER = (-10.5, 24.35)
FAN_COVER_TOP_EAR_HOLE = (-10.5, 27.25)
FAN_COVER_TOP_NOTCH_X_START = -3.0
FAN_COVER_TOP_NOTCH_Y_START = 22.0
FAN_COVER_TOP_NOTCH_CORNER_RADIUS = 2.0
FAN_COVER_BOTTOM_FRONT_STRIP_DEPTH = 11.0
FAN_COVER_BOTTOM_SIDE_STRIP_X_END = -15.0
FAN_COVER_BOTTOM_CORNER_RADIUS = 3.0
FAN_COVER_RIGHT_WALL_BOTTOM = -20.85
FAN_COVER_SIDE_FAN_HOLES = [(5.0, -16.75), (5.0, 18.25), (40.0, -16.75), (40.0, 18.25)]
FAN_COVER_SIDE_FAN_HOLE_DIAMETER = 2.0
FAN_COVER_SIDE_VENT_Y_CENTER = 25.5
FAN_COVER_SIDE_VENT_Z_CENTERS = (2.15, 8.15, 14.15)
FAN_COVER_SIDE_VENT_CENTER_SEPARATION = 22.0
FAN_COVER_SIDE_VENT_WIDTH = 3.0


def fan_cover() -> Part:
    half_width = FAN_COVER_WIDTH / 2
    half_height = FAN_COVER_HEIGHT / 2
    sheet = FAN_COVER_SHEET_THICKNESS
    grille_inner, grille_outer = FAN_COVER_GRILLE_RING_DIAMETERS
    opening = (
        Circle(FAN_COVER_FAN_OPENING_DIAMETER / 2)
        - (Circle(grille_outer / 2) - Circle(grille_inner / 2))
        - Circle(FAN_COVER_GRILLE_HUB_DIAMETER / 2)
        - Rectangle(FAN_COVER_FAN_OPENING_DIAMETER, FAN_COVER_GRILLE_SPOKE_WIDTH)
        - Rectangle(FAN_COVER_GRILLE_SPOKE_WIDTH, FAN_COVER_FAN_OPENING_DIAMETER)
    )
    cover = extrude(Plane.XZ * (Rectangle(FAN_COVER_WIDTH, FAN_COVER_HEIGHT) - opening), -sheet)
    standoff_height = FAN_COVER_FAN_STANDOFF_TOP - sheet
    standoff = Cylinder(FAN_COVER_FAN_STANDOFF_DIAMETER / 2, standoff_height, align=BOTTOM) - Cylinder(
        FAN_COVER_FAN_STANDOFF_HOLE_DIAMETER / 2, standoff_height, align=BOTTOM
    )
    for x, z in FAN_4010_MOUNTING_HOLES:
        cover += Pos(FAN_COVER_FAN_CENTER_X + x, sheet, FAN_COVER_FAN_CENTER_Z + z) * FACE_BACK * standoff
    left_wall_outline = Pos(FAN_COVER_DEPTH / 2, 0) * Rectangle(FAN_COVER_DEPTH, FAN_COVER_HEIGHT) - [
        Pos(FAN_COVER_SIDE_VENT_Y_CENTER, z)
        * SlotCenterToCenter(FAN_COVER_SIDE_VENT_CENTER_SEPARATION, FAN_COVER_SIDE_VENT_WIDTH)
        for z in FAN_COVER_SIDE_VENT_Z_CENTERS
    ]
    cover += Pos(-half_width, 0, 0) * extrude(Plane.YZ * left_wall_outline, sheet)
    right_wall_outline = Pos(0, -half_height) * make_face(
        Polyline(
            (0, 0),
            (FAN_COVER_BOTTOM_FRONT_STRIP_DEPTH, 0),
            (
                FAN_COVER_BOTTOM_FRONT_STRIP_DEPTH,
                FAN_COVER_RIGHT_WALL_BOTTOM + half_height,
            ),
            (FAN_COVER_RIGHT_WALL_DEPTH, FAN_COVER_RIGHT_WALL_BOTTOM + half_height),
            (FAN_COVER_RIGHT_WALL_DEPTH, FAN_COVER_HEIGHT),
            (0, FAN_COVER_HEIGHT),
            close=True,
        )
    )
    right_wall_holes = circles(FAN_COVER_SIDE_FAN_HOLES, FAN_COVER_SIDE_FAN_HOLE_DIAMETER)
    cover += Pos(half_width, 0, 0) * extrude(Plane.YZ * (right_wall_outline - right_wall_holes), -sheet)
    top_notch = Pos(FAN_COVER_TOP_NOTCH_X_START, FAN_COVER_TOP_NOTCH_Y_START) * outline_face(
        [
            (0, FAN_COVER_DEPTH),
            (0, 0),
            (half_width - FAN_COVER_TOP_NOTCH_X_START, 0),
            (half_width - FAN_COVER_TOP_NOTCH_X_START, FAN_COVER_DEPTH),
        ],
        [0, FAN_COVER_TOP_NOTCH_CORNER_RADIUS, 0, 0],
    )
    top_outline = Pos(-half_width, 0) * Rectangle(FAN_COVER_WIDTH, FAN_COVER_DEPTH, align=Align.MIN) - top_notch
    cover += Pos(0, 0, half_height - sheet) * extrude(top_outline, sheet)
    bottom_outline = outline_face(
        [
            (-half_width, 0),
            (half_width, 0),
            (half_width, FAN_COVER_BOTTOM_FRONT_STRIP_DEPTH),
            (FAN_COVER_BOTTOM_SIDE_STRIP_X_END, FAN_COVER_BOTTOM_FRONT_STRIP_DEPTH),
            (FAN_COVER_BOTTOM_SIDE_STRIP_X_END, FAN_COVER_DEPTH),
            (-half_width, FAN_COVER_DEPTH),
        ],
        [0, 0, 0, FAN_COVER_BOTTOM_CORNER_RADIUS, FAN_COVER_BOTTOM_CORNER_RADIUS, 0],
    )
    cover += Pos(0, 0, -half_height) * extrude(bottom_outline, sheet)
    ear_x, ear_z = FAN_COVER_SIDE_EAR_CENTER
    side_ear = (
        Pos(ear_x, ear_z) * Circle(FAN_COVER_EAR_RADIUS)
        + Pos(ear_x, ear_z)
        * Rectangle(
            -half_width - ear_x,
            2 * FAN_COVER_EAR_RADIUS,
            align=(Align.MIN, Align.CENTER),
        )
    ) & Pos(-half_width, ear_z) * Rectangle(
        2 * FAN_COVER_EAR_RADIUS + half_width + ear_x,
        2 * FAN_COVER_EAR_RADIUS,
        align=(Align.MAX, Align.CENTER),
    )
    side_ear -= Pos(*FAN_COVER_SIDE_EAR_HOLE) * Circle(FAN_COVER_EAR_HOLE_DIAMETER / 2)
    ear_x, ear_z = FAN_COVER_TOP_EAR_CENTER
    top_ear_bottom = half_height - sheet
    top_ear = (
        Pos(ear_x, ear_z) * Circle(FAN_COVER_EAR_RADIUS)
        + Pos(ear_x, top_ear_bottom)
        * Rectangle(
            2 * FAN_COVER_EAR_RADIUS,
            ear_z - top_ear_bottom,
            align=(Align.CENTER, Align.MIN),
        )
    ) & Pos(ear_x, top_ear_bottom) * Rectangle(
        2 * FAN_COVER_EAR_RADIUS,
        4 * FAN_COVER_EAR_RADIUS,
        align=(Align.CENTER, Align.MIN),
    )
    top_ear -= Pos(*FAN_COVER_TOP_EAR_HOLE) * Circle(FAN_COVER_EAR_HOLE_DIAMETER / 2)
    cover += Pos(0, FAN_COVER_DEPTH, 0) * extrude(Plane.XZ * (side_ear + top_ear), sheet)
    cover = FAN_COVER_LOCATION * cover
    cover.label = "fan_cover"
    return cover
