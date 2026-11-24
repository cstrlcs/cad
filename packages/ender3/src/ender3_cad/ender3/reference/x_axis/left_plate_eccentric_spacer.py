from build123d import Location, Part

from ender3_cad.ender3.reference.components.dimensions import WHEEL_SPACER_LENGTH
from ender3_cad.ender3.reference.components.eccentric_spacer import eccentric_spacer
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.extruder.dimensions import EXTRUDER_MOTOR_BRACKET_FRONT_Y
from ender3_cad.ender3.reference.x_axis.dimensions import X_BEAM_AXIS_Z

LEFT_PLATE_ECCENTRIC_SPACER_AXIS_X = -115.1
LEFT_PLATE_BACK_SPACER_END_Y = EXTRUDER_MOTOR_BRACKET_FRONT_Y - WHEEL_SPACER_LENGTH
LEFT_PLATE_ECCENTRIC_SPACER_LOCATION = Location(
    (LEFT_PLATE_ECCENTRIC_SPACER_AXIS_X, LEFT_PLATE_BACK_SPACER_END_Y, X_BEAM_AXIS_Z), (-90, 0, -103.332817)
)


def left_plate_eccentric_spacer() -> Part:
    return placed(eccentric_spacer(), LEFT_PLATE_ECCENTRIC_SPACER_LOCATION, "left_plate_eccentric_spacer")
