from build123d import Part

from ender3_cad.colors import PURCHASED_PART_COLOR
from ender3_cad.ender3.reference.electronics.mainboard import mainboard


def mainboard_4_2_7() -> Part:
    board = mainboard()
    board.label = "mainboard_4_2_7"
    board.color = PURCHASED_PART_COLOR
    return board
