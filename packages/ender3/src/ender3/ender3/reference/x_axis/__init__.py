from build123d import Compound

from ender3.ender3.reference.x_axis.left_gantry_plate import left_gantry_plate
from ender3.ender3.reference.x_axis.left_plate_eccentric_spacer import left_plate_eccentric_spacer
from ender3.ender3.reference.x_axis.left_plate_eccentric_wheel import left_plate_eccentric_wheel
from ender3.ender3.reference.x_axis.left_plate_eccentric_wheel_plate_spacer import (
    left_plate_eccentric_wheel_plate_spacer,
)
from ender3.ender3.reference.x_axis.left_plate_lower_wheel import left_plate_lower_wheel
from ender3.ender3.reference.x_axis.left_plate_lower_wheel_back_spacer import left_plate_lower_wheel_back_spacer
from ender3.ender3.reference.x_axis.left_plate_lower_wheel_plate_spacer import left_plate_lower_wheel_plate_spacer
from ender3.ender3.reference.x_axis.left_plate_upper_wheel import left_plate_upper_wheel
from ender3.ender3.reference.x_axis.left_plate_upper_wheel_back_spacer import left_plate_upper_wheel_back_spacer
from ender3.ender3.reference.x_axis.left_plate_upper_wheel_plate_spacer import left_plate_upper_wheel_plate_spacer
from ender3.ender3.reference.x_axis.left_x_belt_end_sleeve import left_x_belt_end_sleeve
from ender3.ender3.reference.x_axis.right_gantry_plate import right_gantry_plate
from ender3.ender3.reference.x_axis.right_plate_eccentric_spacer import right_plate_eccentric_spacer
from ender3.ender3.reference.x_axis.right_plate_eccentric_wheel import right_plate_eccentric_wheel
from ender3.ender3.reference.x_axis.right_plate_lower_wheel import right_plate_lower_wheel
from ender3.ender3.reference.x_axis.right_plate_lower_wheel_plate_spacer import right_plate_lower_wheel_plate_spacer
from ender3.ender3.reference.x_axis.right_plate_upper_wheel import right_plate_upper_wheel
from ender3.ender3.reference.x_axis.right_plate_upper_wheel_plate_spacer import right_plate_upper_wheel_plate_spacer
from ender3.ender3.reference.x_axis.right_x_belt_end_sleeve import right_x_belt_end_sleeve
from ender3.ender3.reference.x_axis.x_beam import x_beam
from ender3.ender3.reference.x_axis.x_belt_tensioner import x_belt_tensioner
from ender3.ender3.reference.x_axis.x_endstop_bracket import x_endstop_bracket
from ender3.ender3.reference.x_axis.x_endstop_switch import x_endstop_switch
from ender3.ender3.reference.x_axis.x_idler_back_bearing import x_idler_back_bearing
from ender3.ender3.reference.x_axis.x_idler_front_bearing import x_idler_front_bearing
from ender3.ender3.reference.x_axis.x_motor import x_motor
from ender3.ender3.reference.x_axis.x_motor_pulley import x_motor_pulley
from ender3.ender3.reference.x_axis.z_nut import z_nut


def x_axis() -> Compound:
    return Compound(
        label="x_axis",
        children=[
            x_beam(),
            left_gantry_plate(),
            right_gantry_plate(),
            x_endstop_bracket(),
            x_belt_tensioner(),
            z_nut(),
            x_motor(),
            x_motor_pulley(),
            x_endstop_switch(),
            left_plate_eccentric_wheel(),
            left_plate_upper_wheel(),
            left_plate_lower_wheel(),
            right_plate_eccentric_wheel(),
            right_plate_upper_wheel(),
            right_plate_lower_wheel(),
            left_plate_eccentric_wheel_plate_spacer(),
            left_plate_upper_wheel_back_spacer(),
            left_plate_upper_wheel_plate_spacer(),
            left_plate_lower_wheel_back_spacer(),
            left_plate_lower_wheel_plate_spacer(),
            right_plate_upper_wheel_plate_spacer(),
            right_plate_lower_wheel_plate_spacer(),
            left_plate_eccentric_spacer(),
            right_plate_eccentric_spacer(),
            x_idler_back_bearing(),
            x_idler_front_bearing(),
            left_x_belt_end_sleeve(),
            right_x_belt_end_sleeve(),
        ],
    )
