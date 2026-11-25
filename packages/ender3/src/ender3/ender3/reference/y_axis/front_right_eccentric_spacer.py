from build123d import Location, Part

from ender3.ender3.reference.components.eccentric_spacer import eccentric_spacer
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.y_axis.dimensions import (
    ECCENTRIC_SPACER_BOSS_END_Z,
    FRONT_RIGHT_ECCENTRIC_SPACER_POSITION,
)

FRONT_RIGHT_ECCENTRIC_SPACER_LOCATION = Location(
    (*FRONT_RIGHT_ECCENTRIC_SPACER_POSITION, ECCENTRIC_SPACER_BOSS_END_Z), (0, 0, -72.825335)
)


def front_right_eccentric_spacer() -> Part:
    return placed(eccentric_spacer(), FRONT_RIGHT_ECCENTRIC_SPACER_LOCATION, "front_right_eccentric_spacer")
