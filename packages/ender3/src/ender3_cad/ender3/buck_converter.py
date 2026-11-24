from build123d import Part

from ender3_cad.colors import PURCHASED_PART_COLOR
from ender3_cad.ender3.purchased.lm2596_module import lm2596_module
from ender3_cad.upgrades.board_cases.dimensions import LM2596_LOCATION


def buck_converter() -> Part:
    converter = LM2596_LOCATION * lm2596_module()
    converter.label = "buck_converter"
    converter.color = PURCHASED_PART_COLOR
    return converter
