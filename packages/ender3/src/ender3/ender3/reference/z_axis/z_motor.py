from build123d import Location, Part

from ender3.ender3.reference.components.stepper_42_34 import stepper_42_34
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.z_axis.dimensions import LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y

Z_MOTOR_LOCATION = Location((LEAD_SCREW_AXIS_X, LEAD_SCREW_AXIS_Y, 73.75), (0, 0, -180))


def z_motor() -> Part:
    return placed(stepper_42_34(), Z_MOTOR_LOCATION, "z_motor")
