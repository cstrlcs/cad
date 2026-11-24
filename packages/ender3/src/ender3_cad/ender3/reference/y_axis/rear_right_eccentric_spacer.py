from build123d import Location, Part

from ender3_cad.ender3.reference.components.eccentric_spacer import eccentric_spacer
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.y_axis.dimensions import (
    ECCENTRIC_SPACER_BOSS_END_Z,
    REAR_RIGHT_ECCENTRIC_SPACER_POSITION,
)

REAR_RIGHT_ECCENTRIC_SPACER_LOCATION = Location(
    (*REAR_RIGHT_ECCENTRIC_SPACER_POSITION, ECCENTRIC_SPACER_BOSS_END_Z), (0, 0, -61.962709)
)


def rear_right_eccentric_spacer() -> Part:
    return placed(eccentric_spacer(), REAR_RIGHT_ECCENTRIC_SPACER_LOCATION, "rear_right_eccentric_spacer")
