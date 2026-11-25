from build123d import Compound

from ender3.ender3.reference.z_axis.z_coupler import z_coupler
from ender3.ender3.reference.z_axis.z_endstop_bracket import z_endstop_bracket
from ender3.ender3.reference.z_axis.z_endstop_switch import z_endstop_switch
from ender3.ender3.reference.z_axis.z_lead_screw import z_lead_screw
from ender3.ender3.reference.z_axis.z_motor import z_motor
from ender3.ender3.reference.z_axis.z_motor_bracket import z_motor_bracket


def z_axis() -> Compound:
    return Compound(
        label="z_axis",
        children=[z_motor(), z_motor_bracket(), z_coupler(), z_lead_screw(), z_endstop_bracket(), z_endstop_switch()],
    )
