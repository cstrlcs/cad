from math import radians, tan

from build123d import Axis, Cylinder, Part, Plane, Polygon, Pos, RegularPolygon, extrude, revolve

from ender3.dimensions import BOTTOM
from ender3.ender3.reference.print_head.dimensions import HOTEND_AXIS_X, HOTEND_AXIS_Y

PNEUMATIC_COUPLER_LOCATION = Pos(HOTEND_AXIS_X, HOTEND_AXIS_Y, 274.092319)
PNEUMATIC_COUPLER_THREAD_DIAMETER = 9.6
PNEUMATIC_COUPLER_THREAD_CHAMFER = 0.5
PNEUMATIC_COUPLER_HEX_ACROSS_FLATS = 10.0
PNEUMATIC_COUPLER_HEX_ROTATION = 16.991
PNEUMATIC_COUPLER_HEX_Z_RANGE = (6.0, 11.5)
PNEUMATIC_COUPLER_HEX_CHAMFER_HALF_ANGLE = 60.0
PNEUMATIC_COUPLER_HEX_ENVELOPE_RADIUS = 6.0
PNEUMATIC_COUPLER_SHOULDER_DIAMETER = 9.8
PNEUMATIC_COUPLER_COLLAR_PROFILE = [
    (4.9, 13.2),
    (4.6, 13.5),
    (4.4, 13.5),
    (4.4, 14.5),
    (3.9, 14.5),
    (3.9, 15.5),
]
PNEUMATIC_COUPLER_HEAD_DIAMETER = 10.8
PNEUMATIC_COUPLER_HEAD_HEIGHT = 1.0
PNEUMATIC_COUPLER_BORE_DIAMETER = 5.3
PNEUMATIC_COUPLER_TUBE_BORE_DIAMETER = 6.8
PNEUMATIC_COUPLER_TUBE_BORE_DEPTH = 6.0
PNEUMATIC_COUPLER_LENGTH = 16.5


def pneumatic_coupler() -> Part:
    thread_radius = PNEUMATIC_COUPLER_THREAD_DIAMETER / 2
    chamfer = PNEUMATIC_COUPLER_THREAD_CHAMFER
    hex_bottom, hex_top = PNEUMATIC_COUPLER_HEX_Z_RANGE
    hex_apothem = PNEUMATIC_COUPLER_HEX_ACROSS_FLATS / 2
    hex_envelope_radius = PNEUMATIC_COUPLER_HEX_ENVELOPE_RADIUS
    chamfer_rise = (hex_envelope_radius - hex_apothem) / tan(radians(PNEUMATIC_COUPLER_HEX_CHAMFER_HALF_ANGLE))
    outer_profile = Plane.XZ * Polygon(
        (0, 0),
        (thread_radius - chamfer, 0),
        (thread_radius, chamfer),
        (thread_radius, hex_bottom),
        (hex_apothem, hex_bottom),
        (hex_envelope_radius, hex_bottom + chamfer_rise),
        (hex_envelope_radius, hex_top - chamfer_rise),
        (hex_apothem, hex_top),
        (PNEUMATIC_COUPLER_SHOULDER_DIAMETER / 2, hex_top),
        *PNEUMATIC_COUPLER_COLLAR_PROFILE,
        (
            PNEUMATIC_COUPLER_HEAD_DIAMETER / 2,
            PNEUMATIC_COUPLER_LENGTH - PNEUMATIC_COUPLER_HEAD_HEIGHT,
        ),
        (PNEUMATIC_COUPLER_HEAD_DIAMETER / 2, PNEUMATIC_COUPLER_LENGTH),
        (0, PNEUMATIC_COUPLER_LENGTH),
        align=None,
    )
    hex_prism = Pos(0, 0, hex_bottom) * extrude(
        RegularPolygon(
            hex_apothem,
            6,
            major_radius=False,
            rotation=PNEUMATIC_COUPLER_HEX_ROTATION,
            align=None,
        ),
        hex_top - hex_bottom,
    )
    round_part = Cylinder(hex_envelope_radius, PNEUMATIC_COUPLER_LENGTH, align=BOTTOM) - Pos(
        0, 0, hex_bottom
    ) * Cylinder(hex_envelope_radius, hex_top - hex_bottom, align=BOTTOM)
    body = revolve(outer_profile, Axis.Z) & (hex_prism + round_part)
    tube_bore_bottom = PNEUMATIC_COUPLER_LENGTH - PNEUMATIC_COUPLER_TUBE_BORE_DEPTH
    body -= Cylinder(PNEUMATIC_COUPLER_BORE_DIAMETER / 2, PNEUMATIC_COUPLER_LENGTH, align=BOTTOM)
    body -= Pos(0, 0, tube_bore_bottom) * Cylinder(
        PNEUMATIC_COUPLER_TUBE_BORE_DIAMETER / 2,
        PNEUMATIC_COUPLER_TUBE_BORE_DEPTH,
        align=BOTTOM,
    )
    body = PNEUMATIC_COUPLER_LOCATION * body
    body.label = "pneumatic_coupler"
    return body
