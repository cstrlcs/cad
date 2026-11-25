from build123d import Axis, Box, Cylinder, Part, Plane, Polygon, Pos, revolve

from ender3.dimensions import BOTTOM, FACE_BACK, FACE_FRONT
from ender3.ender3.reference.print_head.dimensions import (
    HEAT_BLOCK_SCREW_HOLES,
    RADIATOR_LOCATION,
    RADIATOR_MOUNT_HOLES,
)

RADIATOR_DIAMETER = 20.0
RADIATOR_FLAT_WIDTH = 12.0
RADIATOR_HEIGHT = 27.8
RADIATOR_BASE_HEIGHT = 4.0
RADIATOR_CORE_DIAMETER = 8.6
RADIATOR_FIN_COUNT = 9
RADIATOR_FIN_THICKNESS = 0.8
RADIATOR_FIN_PITCH = 1.8
RADIATOR_FIRST_FIN_Z = 5.0
RADIATOR_NECK_DIAMETER = 11.0
RADIATOR_NECK_Z_RANGE = (20.2, 21.2)
RADIATOR_THROAT_BORE_DIAMETER = 7.0
RADIATOR_THROAT_BORE_DEPTH = 16.7
RADIATOR_FILAMENT_BORE_DIAMETER = 5.0
RADIATOR_FILAMENT_BORE_TOP = 18.2
RADIATOR_COUPLER_BORE_DIAMETER = 9.8
RADIATOR_COUPLER_BORE_DEPTH = 8.0
RADIATOR_COUPLER_CONE_DIAMETER = 8.2
RADIATOR_HEAT_BLOCK_SCREW_HOLE_DIAMETER = 2.5
RADIATOR_HEAT_BLOCK_SCREW_HOLE_DEPTH = 4.0
RADIATOR_SET_SCREW_DIAMETER = 2.5
RADIATOR_SET_SCREW_Z = 2.0

RADIATOR_MOUNT_HOLE_DIAMETER = 3.2


def radiator() -> Part:
    radius = RADIATOR_DIAMETER / 2
    flats = Box(RADIATOR_DIAMETER, RADIATOR_FLAT_WIDTH, RADIATOR_HEIGHT, align=BOTTOM)
    fin_z_values = [RADIATOR_FIRST_FIN_Z + k * RADIATOR_FIN_PITCH for k in range(RADIATOR_FIN_COUNT)]
    body = Cylinder(radius, RADIATOR_BASE_HEIGHT, align=BOTTOM)
    body += [Pos(0, 0, z) * Cylinder(radius, RADIATOR_FIN_THICKNESS, align=BOTTOM) for z in fin_z_values]
    neck_bottom, neck_top = RADIATOR_NECK_Z_RANGE
    body += Pos(0, 0, neck_top) * Cylinder(radius, RADIATOR_HEIGHT - neck_top, align=BOTTOM)
    body += Pos(0, 0, RADIATOR_BASE_HEIGHT) * Cylinder(
        RADIATOR_CORE_DIAMETER / 2, neck_bottom - RADIATOR_BASE_HEIGHT, align=BOTTOM
    )
    body += Pos(0, 0, neck_bottom) * Cylinder(RADIATOR_NECK_DIAMETER / 2, neck_top - neck_bottom, align=BOTTOM)
    body &= flats
    coupler_bore_bottom = RADIATOR_HEIGHT - RADIATOR_COUPLER_BORE_DEPTH
    bore_profile = Plane.XZ * Polygon(
        (0, 0),
        (RADIATOR_THROAT_BORE_DIAMETER / 2, 0),
        (RADIATOR_THROAT_BORE_DIAMETER / 2, RADIATOR_THROAT_BORE_DEPTH),
        (RADIATOR_FILAMENT_BORE_DIAMETER / 2, RADIATOR_THROAT_BORE_DEPTH),
        (RADIATOR_FILAMENT_BORE_DIAMETER / 2, RADIATOR_FILAMENT_BORE_TOP),
        (RADIATOR_COUPLER_CONE_DIAMETER / 2, coupler_bore_bottom),
        (RADIATOR_COUPLER_BORE_DIAMETER / 2, coupler_bore_bottom),
        (RADIATOR_COUPLER_BORE_DIAMETER / 2, RADIATOR_HEIGHT),
        (0, RADIATOR_HEIGHT),
        align=None,
    )
    body -= revolve(bore_profile, Axis.Z)
    body -= [
        Pos(x, y, 0)
        * Cylinder(
            RADIATOR_HEAT_BLOCK_SCREW_HOLE_DIAMETER / 2,
            RADIATOR_HEAT_BLOCK_SCREW_HOLE_DEPTH,
            align=BOTTOM,
        )
        for x, y in HEAT_BLOCK_SCREW_HOLES
    ]
    body -= (
        Pos(0, -RADIATOR_FLAT_WIDTH / 2, RADIATOR_SET_SCREW_Z)
        * FACE_BACK
        * Cylinder(RADIATOR_SET_SCREW_DIAMETER / 2, RADIATOR_FLAT_WIDTH / 2, align=BOTTOM)
    )
    body -= [
        Pos(x, 0, z) * FACE_FRONT * Cylinder(RADIATOR_MOUNT_HOLE_DIAMETER / 2, RADIATOR_FLAT_WIDTH)
        for x, z in RADIATOR_MOUNT_HOLES
    ]
    body = RADIATOR_LOCATION * body
    body.label = "radiator"
    return body
