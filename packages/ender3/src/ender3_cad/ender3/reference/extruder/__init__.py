from build123d import Compound

from ender3_cad.ender3.reference.extruder.extruder_bowden_coupler import extruder_bowden_coupler
from ender3_cad.ender3.reference.extruder.extruder_drive_gear import extruder_drive_gear
from ender3_cad.ender3.reference.extruder.extruder_housing import extruder_housing
from ender3_cad.ender3.reference.extruder.extruder_idler_arm import extruder_idler_arm
from ender3_cad.ender3.reference.extruder.extruder_idler_bearing import extruder_idler_bearing
from ender3_cad.ender3.reference.extruder.extruder_motor import extruder_motor
from ender3_cad.ender3.reference.extruder.extruder_motor_bracket import extruder_motor_bracket


def extruder() -> Compound:
    return Compound(
        label="extruder",
        children=[
            extruder_motor(),
            extruder_motor_bracket(),
            extruder_housing(),
            extruder_idler_arm(),
            extruder_drive_gear(),
            extruder_idler_bearing(),
            extruder_bowden_coupler(),
        ],
    )
