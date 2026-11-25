from build123d import Cylinder, Part

from ender3.colors import PRINTED_PART_COLOR
from ender3.dimensions import BOTTOM
from ender3.ender3.reference.components.dimensions import F688_BORE_DIAMETER
from ender3.upgrades.belt_tensioners.dimensions import IDLER_GAP

IDLER_BUSHING_BORE_CLEARANCE = 0.05
IDLER_BUSHING_OUTER_DIAMETER = F688_BORE_DIAMETER - IDLER_BUSHING_BORE_CLEARANCE
IDLER_BUSHING_INNER_DIAMETER = 5.4


def idler_bushing() -> Part:
    bushing = Cylinder(IDLER_BUSHING_OUTER_DIAMETER / 2, IDLER_GAP, align=BOTTOM) - Cylinder(
        IDLER_BUSHING_INNER_DIAMETER / 2, IDLER_GAP, align=BOTTOM
    )
    bushing.label = "idler_bushing"
    bushing.color = PRINTED_PART_COLOR
    return bushing
