from build123d import Location, Part

from ender3_cad.ender3.reference.components.gt2_pulley import gt2_pulley
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import X_BEAM_AXIS_Z, X_MOTOR_AXIS_X

X_MOTOR_PULLEY_LOCATION = Location((X_MOTOR_AXIS_X, -25.35, X_BEAM_AXIS_Z), (90, 0, 19.736669))


def x_motor_pulley() -> Part:
    return placed(gt2_pulley(), X_MOTOR_PULLEY_LOCATION, "x_motor_pulley")
