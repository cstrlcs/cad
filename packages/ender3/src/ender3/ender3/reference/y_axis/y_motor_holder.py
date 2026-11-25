from build123d import Align, Circle, Part, Plane, Polygon, Pos, Rectangle, extrude

from ender3.ender3.reference.components.dimensions import NEMA17_MOUNTING_HOLES
from ender3.ender3.reference.construction import circles, outline_face
from ender3.ender3.reference.y_axis.dimensions import (
    SHEET_BEND_INNER_RADIUS,
    SHEET_BEND_OUTER_RADIUS,
    SHEET_THICKNESS,
    Y_PROFILE_REAR_END,
)

Y_MOTOR_HOLDER_FLANGE_X_RANGE = (-15.2, 18.0)
Y_MOTOR_HOLDER_FLANGE_Z_RANGE = (-19.0, 17.0)
Y_MOTOR_HOLDER_FLANGE_CORNER_RADIUS = 2.0
Y_MOTOR_HOLDER_PROFILE_HOLE_DIAMETER = 5.6
Y_MOTOR_HOLDER_PROFILE_HOLE_OFFSETS = [(-10.0, -10.0), (10.0, -10.0), (10.0, 10.0), (-10.0, 10.0)]
Y_MOTOR_HOLDER_FLANGE_WINDOW_CENTER = (0.0, 8.0)
Y_MOTOR_HOLDER_FLANGE_WINDOW_SIZE = (8.0, 10.0)
Y_MOTOR_HOLDER_PLATE_OUTER_X = -18.0
Y_MOTOR_HOLDER_PLATE_OUTLINE = [
    (2.8, -19.0),
    (58.58578644, -19.0),
    (60.0, -17.58578644),
    (60.0, 31.58578644),
    (58.58578644, 33.0),
    (18.8, 33.0),
    (2.8, 17.0),
]
Y_MOTOR_HOLDER_MOTOR_CENTER = (39.0, 12.0)
Y_MOTOR_HOLDER_MOTOR_BOSS_HOLE_DIAMETER = 24.0
Y_MOTOR_HOLDER_MOTOR_SCREW_HOLE_DIAMETER = 3.5
Y_MOTOR_HOLDER_IDLER_HOLE_CENTER = (15.0, 15.0)
Y_MOTOR_HOLDER_IDLER_HOLE_DIAMETER = 4.2
Y_MOTOR_HOLDER_LOCATION = Pos(*Y_PROFILE_REAR_END)


def y_motor_holder() -> Part:
    (flange_x0, flange_x1), (flange_z0, flange_z1) = Y_MOTOR_HOLDER_FLANGE_X_RANGE, Y_MOTOR_HOLDER_FLANGE_Z_RANGE
    corner_radius = Y_MOTOR_HOLDER_FLANGE_CORNER_RADIUS
    flange_outline = (
        outline_face(
            [(flange_x0, flange_z0), (flange_x1, flange_z0), (flange_x1, flange_z1), (flange_x0, flange_z1)],
            [0, corner_radius, corner_radius, 0],
        )
        - circles(Y_MOTOR_HOLDER_PROFILE_HOLE_OFFSETS, Y_MOTOR_HOLDER_PROFILE_HOLE_DIAMETER)
        - Pos(*Y_MOTOR_HOLDER_FLANGE_WINDOW_CENTER) * Rectangle(*Y_MOTOR_HOLDER_FLANGE_WINDOW_SIZE)
    )
    flange = extrude(Plane.XZ * flange_outline, -SHEET_THICKNESS)
    bend_section = (Circle(SHEET_BEND_OUTER_RADIUS) - Circle(SHEET_BEND_INNER_RADIUS)) & Rectangle(
        SHEET_BEND_OUTER_RADIUS, SHEET_BEND_OUTER_RADIUS, align=Align.MAX
    )
    bend = Pos(flange_x0, SHEET_BEND_OUTER_RADIUS, flange_z0) * extrude(bend_section, flange_z1 - flange_z0)
    motor_center_y, motor_center_z = Y_MOTOR_HOLDER_MOTOR_CENTER
    plate_outline = (
        Polygon(*Y_MOTOR_HOLDER_PLATE_OUTLINE)
        - Pos(*Y_MOTOR_HOLDER_MOTOR_CENTER) * Circle(Y_MOTOR_HOLDER_MOTOR_BOSS_HOLE_DIAMETER / 2)
        - circles(
            [(motor_center_y + y, motor_center_z + z) for y, z in NEMA17_MOUNTING_HOLES],
            Y_MOTOR_HOLDER_MOTOR_SCREW_HOLE_DIAMETER,
        )
        - Pos(*Y_MOTOR_HOLDER_IDLER_HOLE_CENTER) * Circle(Y_MOTOR_HOLDER_IDLER_HOLE_DIAMETER / 2)
    )
    plate = extrude(Plane.YZ.offset(Y_MOTOR_HOLDER_PLATE_OUTER_X) * plate_outline, SHEET_THICKNESS)
    holder = Y_MOTOR_HOLDER_LOCATION * (flange + bend + plate)
    holder.label = "y_motor_holder"
    return holder
