from build123d import Location, Part

from ender3.ender3.reference.components.stepper_42_34 import stepper_42_34
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.x_axis.dimensions import GANTRY_PLATE_BACK_Y, X_BEAM_AXIS_Z, X_MOTOR_AXIS_X

X_MOTOR_LOCATION = Location((X_MOTOR_AXIS_X, GANTRY_PLATE_BACK_Y, X_BEAM_AXIS_Z), (90, 0, 90))


def x_motor() -> Part:
    return placed(stepper_42_34(), X_MOTOR_LOCATION, "x_motor")
