from build123d import Part, Plane

from ender3.colors import PRINTED_PART_COLOR
from ender3.enclosure.brackets.corner_bracket import corner_bracket
from ender3.enclosure.brackets.rail_bracket import rail_bracket
from ender3.enclosure.construction import bracket_joints


def case_brackets() -> list[Part]:
    corner, rail = corner_bracket(), rail_bracket()
    placed = []
    for index, joint in enumerate(bracket_joints(), start=1):
        location = Plane(origin=joint.corner, x_dir=joint.u, z_dir=joint.u.cross(joint.v)).location
        bracket = location * (rail if joint.leg_b_panel == "rail" else corner)
        bracket.label = f"{bracket.label}_{index}"
        bracket.color = PRINTED_PART_COLOR
        placed.append(bracket)
    return placed
