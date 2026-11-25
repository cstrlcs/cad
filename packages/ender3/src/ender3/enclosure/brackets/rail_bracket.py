from build123d import Part, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER, M4_CLEARANCE_DIAMETER
from ender3.enclosure.brackets.construction import bracket_body
from ender3.enclosure.construction import blind_hole, hole
from ender3.enclosure.dimensions import BRACKET_HOLE_OFFSET
from ender3.upgrades.board_cases.dimensions import RAIL_SLOT_CENTERS_Z

RAIL_BRACKET_SLOT_HEIGHT = RAIL_SLOT_CENTERS_Z[0]


def rail_bracket() -> Part:
    bracket = bracket_body()
    bracket -= blind_hole(
        Vector(BRACKET_HOLE_OFFSET, 0, 0), Vector(0, 1, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH
    )
    bracket -= hole(Vector(0, RAIL_BRACKET_SLOT_HEIGHT, 0), Vector(1, 0, 0), M4_CLEARANCE_DIAMETER)
    bracket.label = "rail_bracket"
    bracket.color = PRINTED_PART_COLOR
    return bracket


def rail_bracket_for_printing() -> Part:
    return resting_on_bed(rail_bracket())
