from build123d import Location, Part

from ender3.ender3.reference.components.gt2_pulley_friction_fit import gt2_pulley_friction_fit
from ender3.ender3.reference.construction import placed

Y_MOTOR_PULLEY_LOCATION = Location((-4.5, 164.0, 65.0), (0, 90, 143.829295))


def y_motor_pulley() -> Part:
    return placed(gt2_pulley_friction_fit(), Y_MOTOR_PULLEY_LOCATION, "y_motor_pulley")
