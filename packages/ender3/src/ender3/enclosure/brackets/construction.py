from build123d import Part

from ender3.construction import block
from ender3.enclosure.dimensions import BRACKET_LEG, BRACKET_THICKNESS

BRACKET_WIDTH = 20.0


def bracket_body() -> Part:
    half = BRACKET_WIDTH / 2
    return block((0, BRACKET_LEG), (0, BRACKET_THICKNESS), (-half, half)) + block(
        (0, BRACKET_THICKNESS), (0, BRACKET_LEG), (-half, half)
    )
