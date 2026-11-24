from build123d import Part

from ender3_cad.colors import PURCHASED_PART_COLOR
from ender3_cad.ender3.purchased.raspberry_pi_3b import raspberry_pi_3b
from ender3_cad.upgrades.board_cases.dimensions import PI_LOCATION


def raspberry_pi() -> Part:
    pi = PI_LOCATION * raspberry_pi_3b()
    pi.label = "raspberry_pi"
    pi.color = PURCHASED_PART_COLOR
    return pi
