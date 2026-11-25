from build123d import Location, Part, Plane, Pos, SlotCenterToCenter, extrude

from ender3.ender3.reference.construction import circles
from ender3.ender3.reference.x_axis.dimensions import (
    X_BEAM_AXIS_Y,
    X_BEAM_AXIS_Z,
    X_BEAM_SIZE,
    X_IDLER_AXIS_HEIGHT_ABOVE_BEAM,
    X_IDLER_AXIS_X,
    X_TENSIONER_END_CENTERS_X,
    X_TENSIONER_SCREW_HOLE_DIAMETER,
    X_TENSIONER_SCREW_HOLES_IN_TENSIONER_FRAME,
    X_TENSIONER_WIDTH,
)

X_TENSIONER_FRAME = Pos(0, X_BEAM_AXIS_Y - X_BEAM_SIZE / 2, X_BEAM_AXIS_Z) * Location(Plane.XZ)
X_TENSIONER_THICKNESS = 3.0

X_TENSIONER_IDLER_BOLT_HOLE_DIAMETER = 8.2
X_TENSIONER_IDLER_BOLT_HOLE_IN_TENSIONER_FRAME = (X_IDLER_AXIS_X, X_IDLER_AXIS_HEIGHT_ABOVE_BEAM)


def x_belt_tensioner() -> Part:
    start_x, end_x = X_TENSIONER_END_CENTERS_X
    sketch = (
        Pos((start_x + end_x) / 2, 0) * SlotCenterToCenter(end_x - start_x, X_TENSIONER_WIDTH)
        - circles(X_TENSIONER_SCREW_HOLES_IN_TENSIONER_FRAME, X_TENSIONER_SCREW_HOLE_DIAMETER)
        - circles([X_TENSIONER_IDLER_BOLT_HOLE_IN_TENSIONER_FRAME], X_TENSIONER_IDLER_BOLT_HOLE_DIAMETER)
    )
    tensioner = X_TENSIONER_FRAME * extrude(sketch, X_TENSIONER_THICKNESS)
    tensioner.label = "x_belt_tensioner"
    return tensioner
