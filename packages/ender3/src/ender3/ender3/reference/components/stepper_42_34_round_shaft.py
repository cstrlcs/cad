from build123d import Part

from ender3.ender3.reference.components.dimensions import (
    STEPPER_42_34_BODY_LENGTH,
    STEPPER_42_34_CONNECTOR_HEIGHT,
    STEPPER_42_34_FRONT_CAP_LENGTH,
    STEPPER_42_34_REAR_HOLE_DEPTH,
)
from ender3.ender3.reference.components.nema17_stepper import Nema17Spec, nema17_stepper

STEPPER_42_34_ROUND_SHAFT = Nema17Spec(
    body_length=STEPPER_42_34_BODY_LENGTH,
    front_cap_length=STEPPER_42_34_FRONT_CAP_LENGTH,
    rear_hole_depth=STEPPER_42_34_REAR_HOLE_DEPTH,
    connector_height=STEPPER_42_34_CONNECTOR_HEIGHT,
    shaft_length=23.0,
    shaft_has_flat=False,
)


def stepper_42_34_round_shaft() -> Part:
    motor = nema17_stepper(STEPPER_42_34_ROUND_SHAFT)
    motor.label = "stepper_42_34_round_shaft"
    return motor
