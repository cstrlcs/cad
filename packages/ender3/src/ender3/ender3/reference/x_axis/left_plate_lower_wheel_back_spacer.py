from build123d import Part, Pos

from ender3.dimensions import FACE_FRONT
from ender3.ender3.reference.components.wheel_spacer import wheel_spacer
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.extruder.dimensions import EXTRUDER_MOTOR_BRACKET_FRONT_Y
from ender3.ender3.reference.x_axis.dimensions import LEFT_PLATE_WHEEL_AXIS_X, LOWER_GANTRY_WHEEL_Z

LEFT_PLATE_LOWER_WHEEL_BACK_SPACER_LOCATION = (
    Pos(LEFT_PLATE_WHEEL_AXIS_X, EXTRUDER_MOTOR_BRACKET_FRONT_Y, LOWER_GANTRY_WHEEL_Z) * FACE_FRONT
)


def left_plate_lower_wheel_back_spacer() -> Part:
    return placed(wheel_spacer(), LEFT_PLATE_LOWER_WHEEL_BACK_SPACER_LOCATION, "left_plate_lower_wheel_back_spacer")
