from build123d import Compound

from ender3.ender3.reference.electronics import electronics
from ender3.ender3.reference.extruder import extruder
from ender3.ender3.reference.frame import frame
from ender3.ender3.reference.print_head import print_head
from ender3.ender3.reference.x_axis import x_axis
from ender3.ender3.reference.y_axis import y_axis
from ender3.ender3.reference.z_axis import z_axis


def ender3_pro() -> Compound:
    return Compound(
        label="ender3_pro",
        children=[
            frame(),
            y_axis(),
            z_axis(),
            x_axis(),
            extruder(),
            print_head(),
            electronics(),
        ],
    )
