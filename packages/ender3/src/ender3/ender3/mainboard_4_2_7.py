from build123d import Part

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.reference.electronics.mainboard import mainboard


def mainboard_4_2_7() -> Part:
    board = mainboard()
    board.label = "mainboard_4_2_7"
    board.color = PURCHASED_PART_COLOR
    return board
