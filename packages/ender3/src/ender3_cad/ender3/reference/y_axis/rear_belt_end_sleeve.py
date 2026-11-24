from build123d import Part, Pos

from ender3_cad.ender3.reference.components.belt_end_sleeve import belt_end_sleeve
from ender3_cad.ender3.reference.construction import placed

REAR_BELT_END_SLEEVE_LOCATION = Pos(0.0, 2.09762543, 81.84312861)


def rear_belt_end_sleeve() -> Part:
    return placed(belt_end_sleeve(), REAR_BELT_END_SLEEVE_LOCATION, "rear_belt_end_sleeve")
