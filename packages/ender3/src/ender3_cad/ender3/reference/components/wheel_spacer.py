from build123d import Cylinder, Part

from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.reference.components.dimensions import WHEEL_SPACER_LENGTH

WHEEL_SPACER_OUTER_DIAMETER = 8.0
WHEEL_SPACER_BORE_DIAMETER = 5.5


def wheel_spacer() -> Part:
    spacer = Cylinder(WHEEL_SPACER_OUTER_DIAMETER / 2, WHEEL_SPACER_LENGTH, align=BOTTOM) - Cylinder(
        WHEEL_SPACER_BORE_DIAMETER / 2, WHEEL_SPACER_LENGTH, align=BOTTOM
    )
    spacer.label = "wheel_spacer"
    return spacer
