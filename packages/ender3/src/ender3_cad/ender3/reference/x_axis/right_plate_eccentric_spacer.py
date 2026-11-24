from build123d import Location, Part

from ender3_cad.ender3.reference.components.dimensions import WHEEL_SPACER_LENGTH
from ender3_cad.ender3.reference.components.eccentric_spacer import eccentric_spacer
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import (
    GANTRY_PLATE_BACK_Y,
    RIGHT_PLATE_ECCENTRIC_SPACER_AXIS_X,
    X_BEAM_AXIS_Z,
)

GANTRY_PLATE_SPACER_END_Y = GANTRY_PLATE_BACK_Y + WHEEL_SPACER_LENGTH
RIGHT_PLATE_ECCENTRIC_SPACER_LOCATION = Location(
    (RIGHT_PLATE_ECCENTRIC_SPACER_AXIS_X, GANTRY_PLATE_SPACER_END_Y, X_BEAM_AXIS_Z), (90, 0, -58.369658)
)


def right_plate_eccentric_spacer() -> Part:
    return placed(eccentric_spacer(), RIGHT_PLATE_ECCENTRIC_SPACER_LOCATION, "right_plate_eccentric_spacer")
