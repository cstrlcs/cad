from build123d import Axis, Cylinder, Part, Plane, Polygon, Pos, Rot, revolve

from ender3.dimensions import BOTTOM, FACE_RIGHT
from ender3.ender3.reference.z_axis.dimensions import LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y

Z_COUPLER_BOTTOM_Z = 80.75
Z_COUPLER_LENGTH = 26.0
Z_COUPLER_DIAMETER = 20.0
Z_COUPLER_MOTOR_BORE_DIAMETER = 5.0
Z_COUPLER_MOTOR_BORE_DEPTH = 7.5
Z_COUPLER_LEAD_SCREW_BORE_DIAMETER = 8.0
Z_COUPLER_BOTTOM_CHAMFER = 0.5
Z_COUPLER_TOP_CHAMFER = 0.46
Z_COUPLER_SET_SCREW_HOLE_DIAMETER = 3.4
Z_COUPLER_SET_SCREW_HEIGHTS = (4.0, 22.0)
Z_COUPLER_SET_SCREW_ANGLES = (2.0245, 92.0245)


def z_coupler() -> Part:
    outer_radius = Z_COUPLER_DIAMETER / 2
    motor_bore_radius = Z_COUPLER_MOTOR_BORE_DIAMETER / 2
    screw_bore_radius = Z_COUPLER_LEAD_SCREW_BORE_DIAMETER / 2
    profile = Polygon(
        (motor_bore_radius + Z_COUPLER_BOTTOM_CHAMFER, 0.0),
        (outer_radius - Z_COUPLER_BOTTOM_CHAMFER, 0.0),
        (outer_radius, Z_COUPLER_BOTTOM_CHAMFER),
        (outer_radius, Z_COUPLER_LENGTH - Z_COUPLER_TOP_CHAMFER),
        (outer_radius - Z_COUPLER_TOP_CHAMFER, Z_COUPLER_LENGTH),
        (screw_bore_radius + Z_COUPLER_TOP_CHAMFER, Z_COUPLER_LENGTH),
        (screw_bore_radius, Z_COUPLER_LENGTH - Z_COUPLER_TOP_CHAMFER),
        (screw_bore_radius, Z_COUPLER_MOTOR_BORE_DEPTH),
        (motor_bore_radius, Z_COUPLER_MOTOR_BORE_DEPTH),
        (motor_bore_radius, Z_COUPLER_BOTTOM_CHAMFER),
    )
    set_screws = [
        Rot(0, 0, angle)
        * Pos(0, 0, height)
        * FACE_RIGHT
        * Cylinder(Z_COUPLER_SET_SCREW_HOLE_DIAMETER / 2, outer_radius, align=BOTTOM)
        for height in Z_COUPLER_SET_SCREW_HEIGHTS
        for angle in Z_COUPLER_SET_SCREW_ANGLES
    ]
    coupler = Pos(LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y, Z_COUPLER_BOTTOM_Z) * (
        revolve(Plane.XZ * profile, Axis.Z) - set_screws
    )
    coupler.label = "z_coupler"
    return coupler
