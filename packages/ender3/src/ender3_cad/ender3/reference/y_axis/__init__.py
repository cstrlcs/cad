from build123d import Compound

from ender3_cad.ender3.reference.y_axis.bed_carriage_plate import bed_carriage_plate
from ender3_cad.ender3.reference.y_axis.build_surface import build_surface
from ender3_cad.ender3.reference.y_axis.front_belt_end_sleeve import front_belt_end_sleeve
from ender3_cad.ender3.reference.y_axis.front_left_wheel import front_left_wheel
from ender3_cad.ender3.reference.y_axis.front_left_wheel_spacer import front_left_wheel_spacer
from ender3_cad.ender3.reference.y_axis.front_right_eccentric_spacer import front_right_eccentric_spacer
from ender3_cad.ender3.reference.y_axis.front_right_wheel import front_right_wheel
from ender3_cad.ender3.reference.y_axis.heated_bed import heated_bed
from ender3_cad.ender3.reference.y_axis.rear_belt_end_sleeve import rear_belt_end_sleeve
from ender3_cad.ender3.reference.y_axis.rear_left_wheel import rear_left_wheel
from ender3_cad.ender3.reference.y_axis.rear_left_wheel_spacer import rear_left_wheel_spacer
from ender3_cad.ender3.reference.y_axis.rear_right_eccentric_spacer import rear_right_eccentric_spacer
from ender3_cad.ender3.reference.y_axis.rear_right_wheel import rear_right_wheel
from ender3_cad.ender3.reference.y_axis.y_belt_tensioner import y_belt_tensioner
from ender3_cad.ender3.reference.y_axis.y_belt_tensioner_idler_bushing import y_belt_tensioner_idler_bushing
from ender3_cad.ender3.reference.y_axis.y_endstop_bracket import y_endstop_bracket
from ender3_cad.ender3.reference.y_axis.y_endstop_switch import y_endstop_switch
from ender3_cad.ender3.reference.y_axis.y_front_idler_left_bearing import y_front_idler_left_bearing
from ender3_cad.ender3.reference.y_axis.y_front_idler_right_bearing import y_front_idler_right_bearing
from ender3_cad.ender3.reference.y_axis.y_motor import y_motor
from ender3_cad.ender3.reference.y_axis.y_motor_holder import y_motor_holder
from ender3_cad.ender3.reference.y_axis.y_motor_holder_idler_bushing import y_motor_holder_idler_bushing
from ender3_cad.ender3.reference.y_axis.y_motor_pulley import y_motor_pulley
from ender3_cad.ender3.reference.y_axis.y_rear_idler_left_bearing import y_rear_idler_left_bearing
from ender3_cad.ender3.reference.y_axis.y_rear_idler_right_bearing import y_rear_idler_right_bearing


def y_axis() -> Compound:
    return Compound(
        label="y_axis",
        children=[
            bed_carriage_plate(),
            heated_bed(),
            build_surface(),
            y_motor_holder(),
            y_motor_holder_idler_bushing(),
            y_belt_tensioner(),
            y_belt_tensioner_idler_bushing(),
            y_endstop_bracket(),
            front_belt_end_sleeve(),
            rear_belt_end_sleeve(),
            front_left_wheel(),
            front_right_wheel(),
            rear_right_wheel(),
            rear_left_wheel(),
            front_left_wheel_spacer(),
            rear_left_wheel_spacer(),
            front_right_eccentric_spacer(),
            rear_right_eccentric_spacer(),
            y_front_idler_right_bearing(),
            y_front_idler_left_bearing(),
            y_rear_idler_right_bearing(),
            y_rear_idler_left_bearing(),
            y_motor(),
            y_motor_pulley(),
            y_endstop_switch(),
        ],
    )
