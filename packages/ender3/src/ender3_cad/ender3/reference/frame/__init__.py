from build123d import Compound

from ender3_cad.ender3.reference.frame.left_base_rail import left_base_rail
from ender3_cad.ender3.reference.frame.left_upright import left_upright
from ender3_cad.ender3.reference.frame.middle_cross_member import middle_cross_member
from ender3_cad.ender3.reference.frame.right_base_rail import right_base_rail
from ender3_cad.ender3.reference.frame.right_upright import right_upright
from ender3_cad.ender3.reference.frame.top_bar import top_bar
from ender3_cad.ender3.reference.frame.y_rail import y_rail


def frame() -> Compound:
    return Compound(
        label="frame",
        children=[
            left_base_rail(),
            right_base_rail(),
            middle_cross_member(),
            y_rail(),
            left_upright(),
            right_upright(),
            top_bar(),
        ],
    )
