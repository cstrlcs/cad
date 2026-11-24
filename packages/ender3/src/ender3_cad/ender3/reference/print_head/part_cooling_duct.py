from build123d import Align, Box, Circle, Part, Plane, Pos, Rectangle, Rot, extrude

from ender3_cad.ender3.reference.construction import outline_face

PART_COOLING_DUCT_LOCATION = Pos(38.753014, -72.7, 234.542319)
PART_COOLING_DUCT_LENGTH = 40.0
PART_COOLING_DUCT_PROFILE_WIDTH = 9.977
PART_COOLING_DUCT_PROFILE_TOP = 5.05
PART_COOLING_DUCT_PROFILE = [
    (0.0, 0.0),
    (PART_COOLING_DUCT_PROFILE_WIDTH, 0.0),
    (PART_COOLING_DUCT_PROFILE_WIDTH, PART_COOLING_DUCT_PROFILE_TOP),
    (0.0, PART_COOLING_DUCT_PROFILE_TOP),
]
PART_COOLING_DUCT_PROFILE_RADII = [0.0, 4.977, 0.0, 0.0]
PART_COOLING_DUCT_CHANNEL_X_START = -1.0
PART_COOLING_DUCT_CHANNEL_TOP = 4.25
PART_COOLING_DUCT_CHANNEL_PROFILE = [
    (PART_COOLING_DUCT_CHANNEL_X_START, 0.8),
    (0.785, 0.8),
    (7.5, 3.482),
    (7.5, PART_COOLING_DUCT_CHANNEL_TOP),
    (PART_COOLING_DUCT_CHANNEL_X_START, PART_COOLING_DUCT_CHANNEL_TOP),
]
PART_COOLING_DUCT_CHANNEL_RADII = [0.0, 0.0, 0.6, 0.0, 0.0]
PART_COOLING_DUCT_CHANNEL_Y_RANGE = (-16.5, 15.5)
PART_COOLING_DUCT_INLET_X_RANGE = (0.9, 9.1)
PART_COOLING_DUCT_INLET_INNER_X_END = 7.5
PART_COOLING_DUCT_INLET_HALF_LENGTH = 13.8
PART_COOLING_DUCT_INLET_INNER_HALF_LENGTH = 12.6
PART_COOLING_DUCT_INLET_TOP = 9.05
PART_COOLING_DUCT_EAR_X_RANGE = (3.7, 6.5)
PART_COOLING_DUCT_EAR_WIDTH = 4.6
PART_COOLING_DUCT_EAR_ROUND_CENTER = (17.9, 7.15)
PART_COOLING_DUCT_EAR_RADIUS = 2.5
PART_COOLING_DUCT_EAR_HOLE = (17.5, 7.65)
PART_COOLING_DUCT_EAR_HOLE_DIAMETER = 2.4


def part_cooling_duct() -> Part:
    half_length = PART_COOLING_DUCT_LENGTH / 2
    profile = outline_face(PART_COOLING_DUCT_PROFILE, PART_COOLING_DUCT_PROFILE_RADII)
    duct = Pos(0, half_length, 0) * extrude(Plane.XZ * profile, PART_COOLING_DUCT_LENGTH)
    profile_top = PART_COOLING_DUCT_PROFILE_TOP
    inlet_x_start, inlet_x_end = PART_COOLING_DUCT_INLET_X_RANGE
    inlet_height = PART_COOLING_DUCT_INLET_TOP - profile_top
    duct += Pos(inlet_x_start, -PART_COOLING_DUCT_INLET_HALF_LENGTH, profile_top) * Box(
        inlet_x_end - inlet_x_start,
        2 * PART_COOLING_DUCT_INLET_HALF_LENGTH,
        inlet_height,
        align=Align.MIN,
    )
    ear_x_start, ear_x_end = PART_COOLING_DUCT_EAR_X_RANGE
    ear_round_y, ear_round_z = PART_COOLING_DUCT_EAR_ROUND_CENTER
    ear_outline = (
        Pos(half_length - PART_COOLING_DUCT_EAR_WIDTH, profile_top)
        * Rectangle(
            PART_COOLING_DUCT_EAR_WIDTH,
            ear_round_z - profile_top,
            align=Align.MIN,
        )
        + Pos(ear_round_y, ear_round_z) * Circle(PART_COOLING_DUCT_EAR_RADIUS)
    ) & Pos(half_length, profile_top) * Rectangle(
        PART_COOLING_DUCT_EAR_WIDTH,
        2 * PART_COOLING_DUCT_EAR_RADIUS + ear_round_z,
        align=(Align.MAX, Align.MIN),
    )
    ear_outline -= Pos(*PART_COOLING_DUCT_EAR_HOLE) * Circle(PART_COOLING_DUCT_EAR_HOLE_DIAMETER / 2)
    ear = Pos(ear_x_start, 0, 0) * extrude(Plane.YZ * ear_outline, ear_x_end - ear_x_start)
    duct += ear + Rot(0, 0, 180) * Pos(-ear_x_start - ear_x_end, 0, 0) * ear
    channel_start, channel_end = PART_COOLING_DUCT_CHANNEL_Y_RANGE
    channel_profile = outline_face(PART_COOLING_DUCT_CHANNEL_PROFILE, PART_COOLING_DUCT_CHANNEL_RADII)
    duct -= Pos(0, channel_end, 0) * extrude(Plane.XZ * channel_profile, channel_end - channel_start)
    duct -= Pos(
        PART_COOLING_DUCT_CHANNEL_X_START,
        -PART_COOLING_DUCT_INLET_INNER_HALF_LENGTH,
        PART_COOLING_DUCT_CHANNEL_TOP,
    ) * Box(
        PART_COOLING_DUCT_INLET_INNER_X_END - PART_COOLING_DUCT_CHANNEL_X_START,
        2 * PART_COOLING_DUCT_INLET_INNER_HALF_LENGTH,
        PART_COOLING_DUCT_INLET_TOP - PART_COOLING_DUCT_CHANNEL_TOP,
        align=Align.MIN,
    )
    duct = PART_COOLING_DUCT_LOCATION * duct
    duct.label = "part_cooling_duct"
    return duct
