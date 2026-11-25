from build123d import Axis, Cylinder, Part, Plane, Polygon, Pos, revolve

from ender3.construction import block
from ender3.dimensions import BOTTOM, FACE_LEFT, FACE_RIGHT
from ender3.ender3.reference.print_head.dimensions import HEAT_BLOCK_LOCATION, HEAT_BLOCK_SCREW_HOLES

HEAT_BLOCK_SIZE = (20.0, 20.0, 10.0)
HEAT_BLOCK_Y_START = -14.0
HEAT_BLOCK_NOZZLE_BORE_DIAMETER = 6.0
HEAT_BLOCK_HEATER_BORE_DIAMETER = 6.05
HEAT_BLOCK_HEATER_BORE_CENTER = (-9.5, 5.0)
HEAT_BLOCK_HEATER_SET_SCREW_DIAMETER = 3.0
HEAT_BLOCK_MOUNT_HOLE_DIAMETER = 3.2
HEAT_BLOCK_MOUNT_COUNTERSINK_DIAMETER = 5.6
HEAT_BLOCK_THERMISTOR_HOLE_DIAMETER = 2.0
HEAT_BLOCK_THERMISTOR_HOLE_CENTER = (-2.5, 2.0)
HEAT_BLOCK_THERMISTOR_HOLE_DEPTH = 5.0
HEAT_BLOCK_THERMISTOR_SCREW_DIAMETER = 3.0
HEAT_BLOCK_THERMISTOR_SCREW_CENTER = (-2.5, 5.5)
HEAT_BLOCK_THERMISTOR_SCREW_DEPTH = 4.0


def heat_block() -> Part:
    size_x, size_y, size_z = HEAT_BLOCK_SIZE
    body = block((-size_x / 2, size_x / 2), (HEAT_BLOCK_Y_START, HEAT_BLOCK_Y_START + size_y), (0, size_z))
    body -= Cylinder(HEAT_BLOCK_NOZZLE_BORE_DIAMETER / 2, size_z, align=BOTTOM)
    heater_y, heater_z = HEAT_BLOCK_HEATER_BORE_CENTER
    body -= Pos(0, heater_y, heater_z) * FACE_RIGHT * Cylinder(HEAT_BLOCK_HEATER_BORE_DIAMETER / 2, size_x)
    body -= Pos(0, heater_y, 0) * Cylinder(HEAT_BLOCK_HEATER_SET_SCREW_DIAMETER / 2, heater_z, align=BOTTOM)
    countersink_depth = (HEAT_BLOCK_MOUNT_COUNTERSINK_DIAMETER - HEAT_BLOCK_MOUNT_HOLE_DIAMETER) / 2
    countersunk_hole = Cylinder(HEAT_BLOCK_MOUNT_HOLE_DIAMETER / 2, size_z, align=BOTTOM) + revolve(
        Plane.XZ
        * Polygon(
            (0, 0),
            (HEAT_BLOCK_MOUNT_COUNTERSINK_DIAMETER / 2, 0),
            (HEAT_BLOCK_MOUNT_HOLE_DIAMETER / 2, countersink_depth),
            (0, countersink_depth),
            align=None,
        ),
        Axis.Z,
    )
    body -= [Pos(x, y, 0) * countersunk_hole for x, y in HEAT_BLOCK_SCREW_HOLES]
    for diameter, (y, z), depth in (
        (
            HEAT_BLOCK_THERMISTOR_HOLE_DIAMETER,
            HEAT_BLOCK_THERMISTOR_HOLE_CENTER,
            HEAT_BLOCK_THERMISTOR_HOLE_DEPTH,
        ),
        (
            HEAT_BLOCK_THERMISTOR_SCREW_DIAMETER,
            HEAT_BLOCK_THERMISTOR_SCREW_CENTER,
            HEAT_BLOCK_THERMISTOR_SCREW_DEPTH,
        ),
    ):
        body -= Pos(size_x / 2, y, z) * FACE_LEFT * Cylinder(diameter / 2, depth, align=BOTTOM)
    body = HEAT_BLOCK_LOCATION * body
    body.label = "heat_block"
    return body
