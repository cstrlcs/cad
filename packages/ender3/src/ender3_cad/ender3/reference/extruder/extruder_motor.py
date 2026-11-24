from build123d import Part, Pos

from ender3_cad.ender3.reference.components.stepper_40_42 import stepper_40_42
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.extruder.dimensions import BRACKET_THICKNESS, EXTRUDER_MOUNT_LOCATION

EXTRUDER_MOTOR_LOCATION = EXTRUDER_MOUNT_LOCATION * Pos(0, 0, -BRACKET_THICKNESS)


def extruder_motor() -> Part:
    return placed(stepper_40_42(), EXTRUDER_MOTOR_LOCATION, "extruder_motor")
