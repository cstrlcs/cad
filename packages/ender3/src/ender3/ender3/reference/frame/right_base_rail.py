from build123d import Part, Pos

from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.frame.construction import base_rail

RIGHT_BASE_RAIL_LOCATION = Pos(145, -155, 20)


def right_base_rail() -> Part:
    return placed(base_rail(), RIGHT_BASE_RAIL_LOCATION, "right_base_rail")
