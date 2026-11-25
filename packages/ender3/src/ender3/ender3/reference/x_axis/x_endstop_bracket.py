from build123d import Cone, Cylinder, Location, Part, Plane, Polygon, Pos, Rectangle, RectangleRounded, Sketch, extrude

from ender3.dimensions import BOTTOM
from ender3.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLE_SPACING, NEMA17_MOUNTING_HOLES
from ender3.ender3.reference.construction import circles, range_rectangle
from ender3.ender3.reference.x_axis.dimensions import GANTRY_PLATE_FRONT_Y, X_BEAM_AXIS_Z, X_MOTOR_AXIS_X

X_ENDSTOP_BRACKET_FRAME = Pos(X_MOTOR_AXIS_X, GANTRY_PLATE_FRONT_Y, X_BEAM_AXIS_Z) * Location(Plane.XZ)
X_ENDSTOP_BRACKET_SIZE = 42.0
X_ENDSTOP_BRACKET_CORNER_RADIUS = 5.0
X_ENDSTOP_BRACKET_DEPTH = 34.0
X_ENDSTOP_BRACKET_WALL_THICKNESS = 2.1
X_ENDSTOP_BRACKET_RIB_HEIGHT = 2.9
X_ENDSTOP_BRACKET_SIDE_OPENING_HALF_HEIGHT = 14.1724
X_ENDSTOP_BRACKET_SCREW_HOLE_DIAMETER = 3.1
X_ENDSTOP_BRACKET_COUNTERSINK_DIAMETER = 6.7
X_ENDSTOP_BRACKET_SCREW_TUBE_DIAMETER = 7.3
X_ENDSTOP_BRACKET_SCREW_BOSS_DIAMETER = 10.0
X_ENDSTOP_BRACKET_RIBBED_POCKET_COLUMNS = [
    (-18.9, -14.8871),
    (-13.6871, -9.8871),
    (-8.6871, -4.8871),
    (-3.6871, 0.1129),
    (1.3129, 5.6887),
]
X_ENDSTOP_BRACKET_RIBBED_POCKET_ROWS = [(-18.9, -8.1), (-6.9, -0.6), (0.6, 6.9), (8.1, 18.9)]
X_ENDSTOP_BRACKET_OPEN_POCKET_COLUMNS = [(6.8887, 11.2644), (12.4644, 16.6)]
X_ENDSTOP_BRACKET_OPEN_POCKET_ROWS = [(-18.9, -0.6), (0.6, 18.9)]
X_ENDSTOP_BRACKET_LEVER_NOTCH_X_RANGE = (18.7, 21.0)
X_ENDSTOP_BRACKET_LEVER_NOTCH_HEIGHT = 18.0
X_ENDSTOP_BRACKET_GUSSET_HEIGHT = 6.0
X_ENDSTOP_BRACKET_GUSSET_START_DEPTH = 9.0
X_ENDSTOP_BRACKET_BELT_SLOT_WIDTH = 15.0
X_ENDSTOP_BRACKET_BELT_SLOT_DEPTH = 13.0
X_ENDSTOP_BRACKET_BELT_SLOT_CORNER_RADIUS = 2.0
X_ENDSTOP_SWITCH_POSTS_IN_BRACKET_FRAME = [(7.05, -7.5), (7.05, 7.5)]
X_ENDSTOP_SWITCH_POST_DIAMETER = 7.2
X_ENDSTOP_SWITCH_POST_FLAT_OFFSET = 5.2
X_ENDSTOP_SWITCH_POST_HOLE_DIAMETER = 2.6
X_ENDSTOP_SWITCH_POST_LENGTH = 10.0
X_ENDSTOP_SWITCH_LOCATING_RIBS_IN_BRACKET_FRAME = [
    ((15.7586, 16.6745), (7.1008, 15.5)),
    ((16.164, 16.9434), (-15.5, -8.6641)),
]


def x_endstop_bracket() -> Part:
    half_size = X_ENDSTOP_BRACKET_SIZE / 2
    inner_half_size = half_size - X_ENDSTOP_BRACKET_WALL_THICKNESS
    screw_offset = NEMA17_MOUNTING_HOLE_SPACING / 2
    rib_band_start = X_ENDSTOP_BRACKET_DEPTH - X_ENDSTOP_BRACKET_WALL_THICKNESS - X_ENDSTOP_BRACKET_RIB_HEIGHT
    outline = RectangleRounded(X_ENDSTOP_BRACKET_SIZE, X_ENDSTOP_BRACKET_SIZE, X_ENDSTOP_BRACKET_CORNER_RADIUS)
    switch_posts = (
        Sketch()
        + circles(X_ENDSTOP_SWITCH_POSTS_IN_BRACKET_FRAME, X_ENDSTOP_SWITCH_POST_DIAMETER)
        - Rectangle(X_ENDSTOP_BRACKET_SIZE, 2 * X_ENDSTOP_SWITCH_POST_FLAT_OFFSET)
    )
    switch_holders = switch_posts + [range_rectangle(*rib) for rib in X_ENDSTOP_SWITCH_LOCATING_RIBS_IN_BRACKET_FRAME]
    pockets = [
        range_rectangle(column, row)
        for column in X_ENDSTOP_BRACKET_RIBBED_POCKET_COLUMNS
        for row in X_ENDSTOP_BRACKET_RIBBED_POCKET_ROWS
    ] + [
        range_rectangle(column, row)
        for column in X_ENDSTOP_BRACKET_OPEN_POCKET_COLUMNS
        for row in X_ENDSTOP_BRACKET_OPEN_POCKET_ROWS
    ]
    lever_notch = range_rectangle(
        X_ENDSTOP_BRACKET_LEVER_NOTCH_X_RANGE,
        (-X_ENDSTOP_BRACKET_LEVER_NOTCH_HEIGHT / 2, X_ENDSTOP_BRACKET_LEVER_NOTCH_HEIGHT / 2),
    )
    rib_band = (
        outline
        - pockets
        + circles(NEMA17_MOUNTING_HOLES, X_ENDSTOP_BRACKET_SCREW_BOSS_DIAMETER)
        + switch_posts
        - lever_notch
    )
    channel = (
        outline
        - Rectangle(X_ENDSTOP_BRACKET_SIZE, 2 * X_ENDSTOP_BRACKET_SIDE_OPENING_HALF_HEIGHT)
        - Rectangle(2 * inner_half_size, 2 * inner_half_size)
        + circles(NEMA17_MOUNTING_HOLES, X_ENDSTOP_BRACKET_SCREW_TUBE_DIAMETER)
        + [
            range_rectangle(
                sorted((x_side * screw_offset, x_side * inner_half_size)),
                sorted((z_side * screw_offset, z_side * inner_half_size)),
            )
            for x_side in (-1, 1)
            for z_side in (-1, 1)
        ]
    )
    gussets = [
        Plane.YZ.offset(-half_size)
        * Polygon(
            (side * X_ENDSTOP_BRACKET_SIDE_OPENING_HALF_HEIGHT, rib_band_start),
            (side * (X_ENDSTOP_BRACKET_SIDE_OPENING_HALF_HEIGHT - X_ENDSTOP_BRACKET_GUSSET_HEIGHT), rib_band_start),
            (side * X_ENDSTOP_BRACKET_SIDE_OPENING_HALF_HEIGHT, X_ENDSTOP_BRACKET_GUSSET_START_DEPTH),
        )
        for side in (-1, 1)
    ]
    slot_half_width = X_ENDSTOP_BRACKET_BELT_SLOT_WIDTH / 2
    slot_radius = X_ENDSTOP_BRACKET_BELT_SLOT_CORNER_RADIUS
    belt_slot = (
        range_rectangle((-slot_half_width, slot_half_width), (0, X_ENDSTOP_BRACKET_BELT_SLOT_DEPTH - slot_radius))
        + range_rectangle(
            (-slot_half_width + slot_radius, slot_half_width - slot_radius),
            (0, X_ENDSTOP_BRACKET_BELT_SLOT_DEPTH),
        )
        + circles(
            [
                (side * (slot_half_width - slot_radius), X_ENDSTOP_BRACKET_BELT_SLOT_DEPTH - slot_radius)
                for side in (-1, 1)
            ],
            2 * slot_radius,
        )
        + range_rectangle((-slot_half_width - slot_radius, slot_half_width + slot_radius), (0, slot_radius))
        - circles([(side * (slot_half_width + slot_radius), slot_radius) for side in (-1, 1)], 2 * slot_radius)
    )
    end_wall_inner_depth = X_ENDSTOP_BRACKET_DEPTH - X_ENDSTOP_BRACKET_WALL_THICKNESS
    countersink_depth = (X_ENDSTOP_BRACKET_COUNTERSINK_DIAMETER - X_ENDSTOP_BRACKET_SCREW_HOLE_DIAMETER) / 2
    body = (
        Pos(0, 0, end_wall_inner_depth) * extrude(outline, X_ENDSTOP_BRACKET_WALL_THICKNESS)
        + Pos(0, 0, rib_band_start) * extrude(rib_band, X_ENDSTOP_BRACKET_RIB_HEIGHT)
        + extrude(channel, rib_band_start)
        + Pos(0, 0, end_wall_inner_depth) * extrude(switch_holders, -X_ENDSTOP_SWITCH_POST_LENGTH)
        + [extrude(gusset, X_ENDSTOP_BRACKET_WALL_THICKNESS, dir=(1, 0, 0)) for gusset in gussets]
        - Plane.XZ.offset(inner_half_size) * extrude(belt_slot, X_ENDSTOP_BRACKET_WALL_THICKNESS)
        - [
            Pos(x, z)
            * Cylinder(
                X_ENDSTOP_BRACKET_SCREW_HOLE_DIAMETER / 2,
                X_ENDSTOP_BRACKET_DEPTH,
                align=BOTTOM,
            )
            for x, z in NEMA17_MOUNTING_HOLES
        ]
        - [
            Pos(x, z, X_ENDSTOP_BRACKET_DEPTH - countersink_depth)
            * Cone(
                X_ENDSTOP_BRACKET_SCREW_HOLE_DIAMETER / 2,
                X_ENDSTOP_BRACKET_COUNTERSINK_DIAMETER / 2,
                countersink_depth,
                align=BOTTOM,
            )
            for x, z in NEMA17_MOUNTING_HOLES
        ]
        - [
            Pos(x, z, end_wall_inner_depth - X_ENDSTOP_SWITCH_POST_LENGTH)
            * Cylinder(
                X_ENDSTOP_SWITCH_POST_HOLE_DIAMETER / 2,
                X_ENDSTOP_SWITCH_POST_LENGTH,
                align=BOTTOM,
            )
            for x, z in X_ENDSTOP_SWITCH_POSTS_IN_BRACKET_FRAME
        ]
    )
    bracket = X_ENDSTOP_BRACKET_FRAME * body
    bracket.label = "x_endstop_bracket"
    return bracket
