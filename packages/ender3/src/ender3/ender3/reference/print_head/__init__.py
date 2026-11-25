from build123d import Compound

from ender3.ender3.reference.print_head.fan_cover import fan_cover
from ender3.ender3.reference.print_head.heat_block import heat_block
from ender3.ender3.reference.print_head.hotend_fan import hotend_fan
from ender3.ender3.reference.print_head.lower_eccentric_spacer import lower_eccentric_spacer
from ender3.ender3.reference.print_head.lower_wheel import lower_wheel
from ender3.ender3.reference.print_head.nozzle import nozzle
from ender3.ender3.reference.print_head.part_cooling_duct import part_cooling_duct
from ender3.ender3.reference.print_head.part_cooling_fan import part_cooling_fan
from ender3.ender3.reference.print_head.pneumatic_coupler import pneumatic_coupler
from ender3.ender3.reference.print_head.radiator import radiator
from ender3.ender3.reference.print_head.upper_left_wheel import upper_left_wheel
from ender3.ender3.reference.print_head.upper_left_wheel_spacer import upper_left_wheel_spacer
from ender3.ender3.reference.print_head.upper_right_wheel import upper_right_wheel
from ender3.ender3.reference.print_head.upper_right_wheel_spacer import upper_right_wheel_spacer
from ender3.ender3.reference.print_head.x_carriage_plate import x_carriage_plate


def print_head() -> Compound:
    return Compound(
        label="print_head",
        children=[
            x_carriage_plate(),
            fan_cover(),
            part_cooling_duct(),
            part_cooling_fan(),
            hotend_fan(),
            radiator(),
            heat_block(),
            nozzle(),
            pneumatic_coupler(),
            upper_left_wheel(),
            upper_right_wheel(),
            lower_wheel(),
            upper_left_wheel_spacer(),
            upper_right_wheel_spacer(),
            lower_eccentric_spacer(),
        ],
    )
