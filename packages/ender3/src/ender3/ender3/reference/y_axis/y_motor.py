from build123d import Location, Part

from ender3.ender3.reference.components.stepper_42_34_round_shaft import stepper_42_34_round_shaft
from ender3.ender3.reference.construction import placed

Y_MOTOR_LOCATION = Location((-18.0, 164.0, 65.0), (0, 90, 90))


def y_motor() -> Part:
    return placed(stepper_42_34_round_shaft(), Y_MOTOR_LOCATION, "y_motor")
