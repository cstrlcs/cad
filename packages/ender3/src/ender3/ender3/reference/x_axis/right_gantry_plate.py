from build123d import Part, extrude

from ender3.ender3.reference.construction import circles
from ender3.ender3.reference.x_axis.construction import arc_outline_face
from ender3.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_FRAME,
    GANTRY_PLATE_THICKNESS,
    GANTRY_WHEEL_OFFSET_Z,
    RIGHT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME,
    RIGHT_PLATE_ECCENTRIC_SPACER_AXIS_X,
    RIGHT_PLATE_WHEEL_AXIS_X,
)

RIGHT_PLATE_OUTLINE_POINTS_IN_PLATE_FRAME = [
    (136.0141, 12.929),
    (165.1562, 42.0711),
    (172.2273, 45.0),
    (177.3566, 45.0),
    (187.3566, 35.0),
    (187.3566, 20.0),
    (181.9163, 11.1001),
    (180.8282, 9.3201),
    (180.8282, -9.32),
    (181.9163, -11.1),
    (187.3566, -20.0),
    (187.3566, -35.3788),
    (183.1406, -43.5363),
    (183.0819, -43.578),
    (168.5381, -45.1465),
    (88.3058, -11.0438),
    (84.6017, 8.5714),
    (88.101, 10.0),
    (128.943, 10.0),
]
RIGHT_PLATE_OUTLINE_SEGMENT_RADII = [
    0.0,
    10.0,
    0.0,
    10.0,
    0.0,
    10.0,
    -2.0,
    0.0,
    -2.0,
    10.0,
    0.0,
    10.0,
    0.0,
    15.0,
    0.0,
    12.0,
    5.0,
    0.0,
    -10.0,
]
RIGHT_PLATE_WHEEL_HOLE_DIAMETER = 5.1
RIGHT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME = [
    (RIGHT_PLATE_WHEEL_AXIS_X, -GANTRY_WHEEL_OFFSET_Z),
    (RIGHT_PLATE_WHEEL_AXIS_X, GANTRY_WHEEL_OFFSET_Z),
]
RIGHT_PLATE_ECCENTRIC_WHEEL_HOLE_DIAMETER = 7.2
RIGHT_PLATE_ECCENTRIC_WHEEL_HOLE_IN_PLATE_FRAME = (RIGHT_PLATE_ECCENTRIC_SPACER_AXIS_X, 0.0)
RIGHT_PLATE_BEAM_SCREW_HOLE_DIAMETER = 5.1


def right_gantry_plate() -> Part:
    sketch = (
        arc_outline_face(RIGHT_PLATE_OUTLINE_POINTS_IN_PLATE_FRAME, RIGHT_PLATE_OUTLINE_SEGMENT_RADII)
        - circles(RIGHT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME, RIGHT_PLATE_WHEEL_HOLE_DIAMETER)
        - circles([RIGHT_PLATE_ECCENTRIC_WHEEL_HOLE_IN_PLATE_FRAME], RIGHT_PLATE_ECCENTRIC_WHEEL_HOLE_DIAMETER)
        - circles(RIGHT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME, RIGHT_PLATE_BEAM_SCREW_HOLE_DIAMETER)
    )
    plate = GANTRY_PLATE_FRAME * extrude(sketch, GANTRY_PLATE_THICKNESS, dir=(0, 0, 1))
    plate.label = "right_gantry_plate"
    return plate
