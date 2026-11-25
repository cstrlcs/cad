from build123d import Part

from ender3.ender3.reference.components.nema17_stepper import Nema17Spec, nema17_stepper

STEPPER_40_42 = Nema17Spec(
    body_length=40.0,
    front_cap_length=7.0,
    rear_hole_depth=11.25,
    connector_height=3.0,
    shaft_length=24.0,
    shaft_has_flat=True,
)


def stepper_40_42() -> Part:
    motor = nema17_stepper(STEPPER_40_42)
    motor.label = "stepper_40_42"
    return motor
