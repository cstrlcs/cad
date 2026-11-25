from build123d import Part

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.purchased.raspberry_pi_3b import raspberry_pi_3b
from ender3.upgrades.board_cases.dimensions import PI_LOCATION


def raspberry_pi() -> Part:
    pi = PI_LOCATION * raspberry_pi_3b()
    pi.label = "raspberry_pi"
    pi.color = PURCHASED_PART_COLOR
    return pi
