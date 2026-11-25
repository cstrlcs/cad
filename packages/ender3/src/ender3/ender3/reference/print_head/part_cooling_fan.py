from build123d import Align, Box, Circle, GridLocations, Part, Plane, Pos, RectangleRounded, Rot, Sketch, extrude

from ender3.ender3.reference.construction import outline_face

PART_COOLING_FAN_LOCATION = Pos(40.564126, -72.7, 259.692319)
PART_COOLING_FAN_THICKNESS = 8.889
PART_COOLING_FAN_OUTLINE = [
    (-15.738, -15.61),
    (-20.0, -15.61),
    (-20.0, 15.738),
    (-15.61, 15.738),
    (-15.61, 20.0),
    (15.738, 20.0),
    (15.738, 15.611),
    (20.0, 15.611),
    (20.0, -15.737),
    (15.61, -15.737),
    (15.61, -20.0),
    (-15.738, -20.0),
]
PART_COOLING_FAN_OUTLINE_RADII = [1.648, 0, 0, 1.648, 0, 0, 1.648, 0, 0, 1.648, 0, 0]
PART_COOLING_FAN_FLANGE_SIZE = 40.0
PART_COOLING_FAN_FLANGE_CORNER_RADIUS = 2.667
PART_COOLING_FAN_FLANGE_X_RANGE = (1.0, 1.889)
PART_COOLING_FAN_MOUNT_HOLE_SPACING = 35.0
PART_COOLING_FAN_MOUNT_HOLE_DIAMETER = 2.6
PART_COOLING_FAN_BACK_WALL = 0.889
PART_COOLING_FAN_FRONT_WALL = 0.889
PART_COOLING_FAN_BORE_DIAMETER = 37.6
PART_COOLING_FAN_INLET_DIAMETER = 31.111
PART_COOLING_FAN_INLET_CENTER = (0.444, 0.0)
PART_COOLING_FAN_HUB_DIAMETER = 20.0
PART_COOLING_FAN_OUTLET_X_START = 1.422
PART_COOLING_FAN_OUTLET_Y_RANGE = (-15.556, 12.889)
PART_COOLING_FAN_OUTLET_HEIGHT = 1.245
PART_COOLING_FAN_WIRE_NOTCH_X_START = 2.889
PART_COOLING_FAN_WIRE_NOTCH = ((17.154, -14.891), (20.0, -13.73))
PART_COOLING_FAN_BLADE_PITCH_ANGLE = 35.0
PART_COOLING_FAN_BLADE_GROUPS = [(-151.32, 6), (68.68, 4)]
PART_COOLING_FAN_BLADE_ANGLES = [
    first_angle + PART_COOLING_FAN_BLADE_PITCH_ANGLE * k
    for first_angle, count in PART_COOLING_FAN_BLADE_GROUPS
    for k in range(count)
]
PART_COOLING_FAN_BLADE_CONCAVE_RADIUS = 12.717
PART_COOLING_FAN_BLADE_CONCAVE_OFFSET = 12.291
PART_COOLING_FAN_BLADE_CONVEX_RADIUS = 15.125
PART_COOLING_FAN_BLADE_CONVEX_OFFSET = 13.68
PART_COOLING_FAN_BLADE_CONVEX_ANGLE_SHIFT = 2.26


def part_cooling_fan() -> Part:
    fan_plane = Plane.YZ
    frame = extrude(
        fan_plane * outline_face(PART_COOLING_FAN_OUTLINE, PART_COOLING_FAN_OUTLINE_RADII),
        PART_COOLING_FAN_THICKNESS,
    )
    flange_start, flange_end = PART_COOLING_FAN_FLANGE_X_RANGE
    flange_outline = RectangleRounded(
        PART_COOLING_FAN_FLANGE_SIZE, PART_COOLING_FAN_FLANGE_SIZE, PART_COOLING_FAN_FLANGE_CORNER_RADIUS
    ) - GridLocations(PART_COOLING_FAN_MOUNT_HOLE_SPACING, PART_COOLING_FAN_MOUNT_HOLE_SPACING, 2, 2) * Circle(
        PART_COOLING_FAN_MOUNT_HOLE_DIAMETER / 2
    )
    frame += Pos(flange_start, 0, 0) * extrude(fan_plane * flange_outline, flange_end - flange_start)
    cavity_depth = PART_COOLING_FAN_THICKNESS - PART_COOLING_FAN_BACK_WALL - PART_COOLING_FAN_FRONT_WALL
    frame -= Pos(PART_COOLING_FAN_BACK_WALL, 0, 0) * extrude(
        fan_plane * Circle(PART_COOLING_FAN_BORE_DIAMETER / 2), cavity_depth
    )
    frame -= Pos(PART_COOLING_FAN_THICKNESS - PART_COOLING_FAN_FRONT_WALL, 0, 0) * extrude(
        fan_plane * Pos(*PART_COOLING_FAN_INLET_CENTER) * Circle(PART_COOLING_FAN_INLET_DIAMETER / 2),
        PART_COOLING_FAN_FRONT_WALL,
    )
    outlet_y_start, outlet_y_end = PART_COOLING_FAN_OUTLET_Y_RANGE
    outlet_length = PART_COOLING_FAN_THICKNESS - PART_COOLING_FAN_FRONT_WALL - PART_COOLING_FAN_OUTLET_X_START
    outlet_corner = Pos(
        PART_COOLING_FAN_OUTLET_X_START,
        outlet_y_start,
        -PART_COOLING_FAN_FLANGE_SIZE / 2,
    )
    frame -= outlet_corner * Box(
        outlet_length,
        outlet_y_end - outlet_y_start,
        PART_COOLING_FAN_FLANGE_SIZE / 2,
        align=Align.MIN,
    )
    (notch_y_start, notch_z_start), (notch_y_end, notch_z_end) = PART_COOLING_FAN_WIRE_NOTCH
    frame -= Pos(PART_COOLING_FAN_WIRE_NOTCH_X_START, notch_y_start, notch_z_start) * Box(
        PART_COOLING_FAN_THICKNESS - PART_COOLING_FAN_WIRE_NOTCH_X_START,
        notch_y_end - notch_y_start,
        notch_z_end - notch_z_start,
        align=Align.MIN,
    )
    ring = Circle(PART_COOLING_FAN_BORE_DIAMETER / 2) - Circle(PART_COOLING_FAN_HUB_DIAMETER / 2)
    angles = PART_COOLING_FAN_BLADE_ANGLES
    gaps = Sketch()
    for index, angle in enumerate(angles):
        next_blade_angle = angles[(index + 1) % len(angles)] + PART_COOLING_FAN_BLADE_CONVEX_ANGLE_SHIFT
        gap = ring & Rot(0, 0, angle) * Pos(PART_COOLING_FAN_BLADE_CONCAVE_OFFSET, 0) * Circle(
            PART_COOLING_FAN_BLADE_CONCAVE_RADIUS
        )
        gaps += gap - Rot(0, 0, next_blade_angle) * Pos(PART_COOLING_FAN_BLADE_CONVEX_OFFSET, 0) * Circle(
            PART_COOLING_FAN_BLADE_CONVEX_RADIUS
        )
    rotor = Circle(PART_COOLING_FAN_BORE_DIAMETER / 2) - gaps
    frame += Pos(PART_COOLING_FAN_BACK_WALL, 0, 0) * extrude(fan_plane * rotor, cavity_depth)
    frame -= outlet_corner * Box(
        outlet_length,
        outlet_y_end - outlet_y_start,
        PART_COOLING_FAN_OUTLET_HEIGHT,
        align=Align.MIN,
    )
    frame = PART_COOLING_FAN_LOCATION * frame
    frame.label = "part_cooling_fan"
    return frame
