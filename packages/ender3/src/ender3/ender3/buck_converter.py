from build123d import Part

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.purchased.lm2596_module import lm2596_module
from ender3.upgrades.board_cases.dimensions import LM2596_LOCATION


def buck_converter() -> Part:
    converter = LM2596_LOCATION * lm2596_module()
    converter.label = "buck_converter"
    converter.color = PURCHASED_PART_COLOR
    return converter
