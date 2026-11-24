from build123d import Cylinder, Location, Part

from ender3_cad.dimensions import FACE_RIGHT
from ender3_cad.ender3.reference.construction import placed

STOCK_IDLER_BUSHING_OUTER_DIAMETER = 8.0
STOCK_IDLER_BUSHING_INNER_DIAMETER = 5.0


def stock_idler_bushing(length: float, location: Location, label: str) -> Part:
    bushing = Cylinder(STOCK_IDLER_BUSHING_OUTER_DIAMETER / 2, length) - Cylinder(
        STOCK_IDLER_BUSHING_INNER_DIAMETER / 2, length
    )
    return placed(FACE_RIGHT * bushing, location, label)
