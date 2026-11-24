from build123d import Part

from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.frame.construction import base_rail
from ender3_cad.ender3.reference.frame.dimensions import LEFT_BASE_RAIL_LOCATION


def left_base_rail() -> Part:
    return placed(base_rail(), LEFT_BASE_RAIL_LOCATION, "left_base_rail")
