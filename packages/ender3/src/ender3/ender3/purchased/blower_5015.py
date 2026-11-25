from math import atan2, degrees

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Cylinder,
    GeomType,
    Keep,
    Part,
    Plane,
    Pos,
    Rectangle,
    SlotCenterToCenter,
    Vector,
    chamfer,
    extrude,
    fillet,
    offset,
    split,
)

from ender3.dimensions import BOTTOM

BLOWER_5015_THICKNESS = 15.0
BLOWER_5015_FLOOR_THICKNESS = 1.8
BLOWER_5015_CEILING_THICKNESS = 1.0
BLOWER_5015_WALL_THICKNESS = 1.2
BLOWER_5015_EDGE_CHAMFER = 0.3
BLOWER_5015_ROTOR_CENTER = (17.15, 25.4)
BLOWER_5015_INTAKE_DIAMETER = 31.0
BLOWER_5015_OUTLET_WIDTH = 20.0
BLOWER_5015_OUTLET_OPENING_WIDTH = BLOWER_5015_OUTLET_WIDTH - 2 * BLOWER_5015_WALL_THICKNESS
BLOWER_5015_OUTLET_OPENING_HEIGHT = BLOWER_5015_THICKNESS - BLOWER_5015_FLOOR_THICKNESS - BLOWER_5015_CEILING_THICKNESS
BLOWER_5015_VOLUTE_RADIUS = 25.0
BLOWER_5015_VOLUTE_FAR_SIDE_CENTER = (16.30755, 26.0142)
BLOWER_5015_VOLUTE_OUTLET_SIDE_CENTER = (14.99038, 26.09345)
BLOWER_5015_VOLUTE_TONGUE_SIDE_CENTER = (18.30344, 25.79764)
BLOWER_5015_VOLUTE_TONGUE_SIDE_RADIUS = 23.0
BLOWER_5015_OUTLET_SIDE_FILLET_RADIUS = 2.0
BLOWER_5015_FAR_SIDE_FILLET_RADIUS = 3.0
BLOWER_5015_MOUNTING_HOLES = [(-5.85, 45.4), (37.15, 7.4)]
BLOWER_5015_MOUNTING_HOLE_DIAMETER = 4.5
BLOWER_5015_EAR_DIAMETER = 6.5
BLOWER_5015_HUB_DIAMETER = 26.0
BLOWER_5015_HUB_TOP_CHAMFER = 1.0
BLOWER_5015_HUB_TOP_EDGE_ROUND = 1.0
BLOWER_5015_IMPELLER_DIAMETER = 42.1682
BLOWER_5015_IMPELLER_DISC_BOTTOM = 4.0
BLOWER_5015_IMPELLER_DISC_THICKNESS = 1.0
BLOWER_5015_LATCH_PROTRUSION = 1.3
BLOWER_5015_LATCH_Y = (1.9, 12.5)
BLOWER_5015_LATCH_Z = (6.0, 9.0)
BLOWER_5015_LATCH_EDGE_ROUND = 0.5


def blower_5015() -> Part:
    rotor_x, rotor_y = BLOWER_5015_ROTOR_CENTER
    hole_a, hole_b = (Vector(*hole) for hole in BLOWER_5015_MOUNTING_HOLES)
    ear_axis = hole_b - hole_a
    ears = Pos(*((hole_a + hole_b) / 2)) * SlotCenterToCenter(
        ear_axis.length, BLOWER_5015_EAR_DIAMETER, rotation=degrees(atan2(ear_axis.Y, ear_axis.X))
    )
    far_side = Plane(origin=hole_a, z_dir=(-ear_axis.Y, ear_axis.X, 0))
    above_rotor = Plane(origin=(rotor_x, rotor_y), z_dir=(0, 1, 0))
    right_of_rotor = Plane(origin=(rotor_x, rotor_y), z_dir=(1, 0, 0))

    far_side_scroll = split(Pos(*BLOWER_5015_VOLUTE_FAR_SIDE_CENTER) * Circle(BLOWER_5015_VOLUTE_RADIUS), far_side)
    outlet_side_scroll = split(
        split(Pos(*BLOWER_5015_VOLUTE_OUTLET_SIDE_CENTER) * Circle(BLOWER_5015_VOLUTE_RADIUS), above_rotor)
        + split(
            Pos(*BLOWER_5015_VOLUTE_TONGUE_SIDE_CENTER) * Circle(BLOWER_5015_VOLUTE_TONGUE_SIDE_RADIUS),
            above_rotor,
            keep=Keep.BOTTOM,
        )
        + Rectangle(BLOWER_5015_OUTLET_WIDTH, rotor_y, align=(Align.CENTER, Align.MIN)),
        far_side,
        keep=Keep.BOTTOM,
    )
    outline = offset(
        offset(far_side_scroll + ears, BLOWER_5015_FAR_SIDE_FILLET_RADIUS), -BLOWER_5015_FAR_SIDE_FILLET_RADIUS
    ) + offset(
        offset(outlet_side_scroll + ears, BLOWER_5015_OUTLET_SIDE_FILLET_RADIUS),
        -BLOWER_5015_OUTLET_SIDE_FILLET_RADIUS,
    )

    tongue_radius = BLOWER_5015_OUTLET_SIDE_FILLET_RADIUS + BLOWER_5015_WALL_THICKNESS
    tongue_side_cavity = split(
        Pos(*BLOWER_5015_VOLUTE_TONGUE_SIDE_CENTER)
        * Circle(BLOWER_5015_VOLUTE_TONGUE_SIDE_RADIUS - BLOWER_5015_WALL_THICKNESS),
        above_rotor,
        keep=Keep.BOTTOM,
    ) + Rectangle(BLOWER_5015_OUTLET_OPENING_WIDTH, rotor_y, align=(Align.CENTER, Align.MIN))
    cavity = offset(offset(tongue_side_cavity, tongue_radius), -tongue_radius) + split(
        split(
            Pos(*BLOWER_5015_VOLUTE_FAR_SIDE_CENTER) * Circle(BLOWER_5015_VOLUTE_RADIUS - BLOWER_5015_WALL_THICKNESS),
            right_of_rotor,
        )
        + split(
            Pos(*BLOWER_5015_VOLUTE_OUTLET_SIDE_CENTER)
            * Circle(BLOWER_5015_VOLUTE_RADIUS - BLOWER_5015_WALL_THICKNESS),
            right_of_rotor,
            keep=Keep.BOTTOM,
        ),
        above_rotor,
    )

    housing = extrude(outline, BLOWER_5015_THICKNESS)
    outlet_end_edges = housing.faces().sort_by(Axis.Y)[0].edges()
    housing = chamfer(housing.faces().filter_by(Axis.Z).edges() - outlet_end_edges, BLOWER_5015_EDGE_CHAMFER)
    housing -= Pos(0, 0, BLOWER_5015_FLOOR_THICKNESS) * extrude(cavity, BLOWER_5015_OUTLET_OPENING_HEIGHT)
    housing -= Pos(rotor_x, rotor_y, BLOWER_5015_THICKNESS - BLOWER_5015_CEILING_THICKNESS) * Cylinder(
        BLOWER_5015_INTAKE_DIAMETER / 2, BLOWER_5015_CEILING_THICKNESS, align=BOTTOM
    )
    for x, y in BLOWER_5015_MOUNTING_HOLES:
        housing -= Pos(x, y, 0) * Cylinder(BLOWER_5015_MOUNTING_HOLE_DIAMETER / 2, BLOWER_5015_THICKNESS, align=BOTTOM)

    hub = Cylinder(BLOWER_5015_HUB_DIAMETER / 2, BLOWER_5015_THICKNESS - BLOWER_5015_FLOOR_THICKNESS, align=BOTTOM)
    hub = chamfer(hub.edges().group_by(Axis.Z)[-1], BLOWER_5015_HUB_TOP_CHAMFER)
    hub = fillet(
        hub.faces().filter_by(GeomType.CONE).edges().filter_by(GeomType.CIRCLE), BLOWER_5015_HUB_TOP_EDGE_ROUND
    )
    impeller_disc = Pos(0, 0, BLOWER_5015_IMPELLER_DISC_BOTTOM) * Cylinder(
        BLOWER_5015_IMPELLER_DIAMETER / 2, BLOWER_5015_IMPELLER_DISC_THICKNESS, align=BOTTOM
    )
    latch = Pos(-BLOWER_5015_OUTLET_WIDTH / 2, BLOWER_5015_LATCH_Y[0], BLOWER_5015_LATCH_Z[0]) * Box(
        BLOWER_5015_LATCH_PROTRUSION,
        BLOWER_5015_LATCH_Y[1] - BLOWER_5015_LATCH_Y[0],
        BLOWER_5015_LATCH_Z[1] - BLOWER_5015_LATCH_Z[0],
        align=(Align.MAX, Align.MIN, Align.MIN),
    )
    latch = fillet(latch.edges().group_by(Axis.X)[0] + latch.edges().filter_by(Axis.X), BLOWER_5015_LATCH_EDGE_ROUND)

    blower = (
        housing
        + Pos(rotor_x, rotor_y, BLOWER_5015_FLOOR_THICKNESS) * hub
        + Pos(rotor_x, rotor_y, 0) * impeller_disc
        + latch
    )
    blower.label = "blower_5015"
    return blower
