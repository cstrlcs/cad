from build123d import Part, extrude

from ender3_cad.ender3.reference.construction import circles
from ender3_cad.ender3.reference.x_axis.construction import arc_outline_face
from ender3_cad.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_FRAME,
    GANTRY_PLATE_THICKNESS,
    GANTRY_WHEEL_OFFSET_Z,
    LEFT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME,
    LEFT_PLATE_WHEEL_AXIS_X,
    X_MOTOR_AXIS_X,
    X_MOTOR_SCREW_HOLES_IN_PLATE_FRAME,
)

LEFT_PLATE_OUTLINE_POINTS_IN_PLATE_FRAME = [
    (-103.2, 0.0),
    (-109.1637, -10.3712),
    (-120.2303, -16.8123),
    (-125.2, -25.455),
    (-125.2, -37.0),
    (-135.2, -47.0),
    (-175.2, -47.0),
    (-181.8517, -44.8811),
    (-208.7483, -25.8101),
    (-212.9642, -17.6526),
    (-212.9642, 15.9197),
    (-209.1986, 23.7384),
    (-182.6813, 44.8825),
    (-163.2, 35.5),
    (-163.2, 22.0),
    (-151.2, 10.0),
    (-112.3716, 10.0),
    (-103.8863, 4.0),
]
LEFT_PLATE_OUTLINE_SEGMENT_RADII = [
    12.0,
    0.0,
    -10.0,
    0.0,
    10.0,
    0.0,
    11.5,
    0.0,
    10.0,
    0.0,
    10.0,
    0.0,
    12.0,
    0.0,
    -12.0,
    0.0,
    9.0,
    12.0,
]
LEFT_PLATE_WHEEL_HOLE_DIAMETER = 5.1
LEFT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME = [
    (LEFT_PLATE_WHEEL_AXIS_X, -GANTRY_WHEEL_OFFSET_Z),
    (LEFT_PLATE_WHEEL_AXIS_X, GANTRY_WHEEL_OFFSET_Z),
]
LEFT_PLATE_ECCENTRIC_WHEEL_HOLE_DIAMETER = 5.2
LEFT_PLATE_ECCENTRIC_WHEEL_HOLE_IN_PLATE_FRAME = (-114.7, -0.5744)
LEFT_PLATE_BEAM_SCREW_HOLE_DIAMETER = 4.5

X_MOTOR_BORE_DIAMETER = 23.0

X_MOTOR_SCREW_HOLE_DIAMETER = 3.5


def left_gantry_plate() -> Part:
    sketch = (
        arc_outline_face(LEFT_PLATE_OUTLINE_POINTS_IN_PLATE_FRAME, LEFT_PLATE_OUTLINE_SEGMENT_RADII)
        - circles(LEFT_PLATE_WHEEL_HOLES_IN_PLATE_FRAME, LEFT_PLATE_WHEEL_HOLE_DIAMETER)
        - circles([LEFT_PLATE_ECCENTRIC_WHEEL_HOLE_IN_PLATE_FRAME], LEFT_PLATE_ECCENTRIC_WHEEL_HOLE_DIAMETER)
        - circles(LEFT_PLATE_BEAM_SCREW_HOLES_IN_PLATE_FRAME, LEFT_PLATE_BEAM_SCREW_HOLE_DIAMETER)
        - circles([(X_MOTOR_AXIS_X, 0.0)], X_MOTOR_BORE_DIAMETER)
        - circles(X_MOTOR_SCREW_HOLES_IN_PLATE_FRAME, X_MOTOR_SCREW_HOLE_DIAMETER)
    )
    plate = GANTRY_PLATE_FRAME * extrude(sketch, GANTRY_PLATE_THICKNESS, dir=(0, 0, 1))
    plate.label = "left_gantry_plate"
    return plate
