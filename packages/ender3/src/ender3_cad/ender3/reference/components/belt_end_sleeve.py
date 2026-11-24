from build123d import Cylinder, Part

from ender3_cad.dimensions import BOTTOM

BELT_END_SLEEVE_OUTER_DIAMETER = 8.0
BELT_END_SLEEVE_INNER_DIAMETER = 7.2
BELT_END_SLEEVE_HEIGHT = 6.0


def belt_end_sleeve() -> Part:
    sleeve = Cylinder(BELT_END_SLEEVE_OUTER_DIAMETER / 2, BELT_END_SLEEVE_HEIGHT, align=BOTTOM) - Cylinder(
        BELT_END_SLEEVE_INNER_DIAMETER / 2, BELT_END_SLEEVE_HEIGHT, align=BOTTOM
    )
    sleeve.label = "belt_end_sleeve"
    return sleeve
