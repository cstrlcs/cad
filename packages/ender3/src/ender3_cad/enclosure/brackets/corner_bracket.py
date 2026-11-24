from build123d import Part, Vector

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import resting_on_bed
from ender3_cad.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3_cad.enclosure.brackets.construction import bracket_body
from ender3_cad.enclosure.construction import blind_hole
from ender3_cad.enclosure.dimensions import BRACKET_HOLE_OFFSET


def corner_bracket() -> Part:
    bracket = bracket_body()
    bracket -= blind_hole(
        Vector(BRACKET_HOLE_OFFSET, 0, 0), Vector(0, 1, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
    )
    bracket -= blind_hole(
        Vector(0, BRACKET_HOLE_OFFSET, 0), Vector(1, 0, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
    )
    bracket.label = "corner_bracket"
    bracket.color = PRINTED_PART_COLOR
    return bracket


def corner_bracket_for_printing() -> Part:
    return resting_on_bed(corner_bracket())
