from math import radians, tan

from build123d import Axis, Cylinder, Part, Plane, Polygon, Pos, RegularPolygon, extrude, revolve

from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.reference.print_head.dimensions import HOTEND_AXIS_X, HOTEND_AXIS_Y

NOZZLE_TIP = (HOTEND_AXIS_X, HOTEND_AXIS_Y, 229.292319)
NOZZLE_LOCATION = Pos(*NOZZLE_TIP)
NOZZLE_HEX_ACROSS_FLATS = 6.0
NOZZLE_HEX_ROTATION = 3.978
NOZZLE_HEX_TOP = 8.0
NOZZLE_TIP_DIAMETER = 0.9
NOZZLE_TIP_HALF_ANGLE = 37.0
NOZZLE_NECK_DIAMETER = 5.0
NOZZLE_THREAD_DIAMETER = 6.0
NOZZLE_THREAD_Z_RANGE = (9.0, 12.5)
NOZZLE_LENGTH = 13.0
NOZZLE_TOP_CHAMFER = 0.5
NOZZLE_ORIFICE_DIAMETER = 0.4
NOZZLE_ORIFICE_LENGTH = 0.8
NOZZLE_BORE_DIAMETER = 2.0
NOZZLE_BORE_BOTTOM = 1.6


def nozzle() -> Part:
    tip_radius = NOZZLE_TIP_DIAMETER / 2
    cone_top_radius = tip_radius + NOZZLE_HEX_TOP * tan(radians(NOZZLE_TIP_HALF_ANGLE))
    thread_bottom, thread_top = NOZZLE_THREAD_Z_RANGE
    thread_radius = NOZZLE_THREAD_DIAMETER / 2
    outer_profile = Plane.XZ * Polygon(
        (0, 0),
        (tip_radius, 0),
        (cone_top_radius, NOZZLE_HEX_TOP),
        (NOZZLE_NECK_DIAMETER / 2, NOZZLE_HEX_TOP),
        (NOZZLE_NECK_DIAMETER / 2, thread_bottom),
        (thread_radius, thread_bottom),
        (thread_radius, thread_top),
        (thread_radius - NOZZLE_TOP_CHAMFER, NOZZLE_LENGTH),
        (0, NOZZLE_LENGTH),
        align=None,
    )
    hex_prism = extrude(
        RegularPolygon(
            NOZZLE_HEX_ACROSS_FLATS / 2,
            6,
            major_radius=False,
            rotation=NOZZLE_HEX_ROTATION,
            align=None,
        ),
        NOZZLE_HEX_TOP,
    )
    upper = Pos(0, 0, NOZZLE_HEX_TOP) * Cylinder(thread_radius, NOZZLE_LENGTH - NOZZLE_HEX_TOP, align=BOTTOM)
    bore_radius = NOZZLE_BORE_DIAMETER / 2
    orifice_radius = NOZZLE_ORIFICE_DIAMETER / 2
    bore_profile = Plane.XZ * Polygon(
        (0, 0),
        (orifice_radius, 0),
        (orifice_radius, NOZZLE_ORIFICE_LENGTH),
        (bore_radius, NOZZLE_BORE_BOTTOM),
        (bore_radius, NOZZLE_LENGTH - NOZZLE_TOP_CHAMFER),
        (bore_radius + NOZZLE_TOP_CHAMFER, NOZZLE_LENGTH),
        (0, NOZZLE_LENGTH),
        align=None,
    )
    body = revolve(outer_profile, Axis.Z) & (hex_prism + upper)
    body -= revolve(bore_profile, Axis.Z)
    body = NOZZLE_LOCATION * body
    body.label = "nozzle"
    return body
