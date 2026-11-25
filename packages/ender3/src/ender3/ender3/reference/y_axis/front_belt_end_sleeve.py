from build123d import Part, Pos

from ender3.ender3.reference.components.belt_end_sleeve import belt_end_sleeve
from ender3.ender3.reference.construction import placed

FRONT_BELT_END_SLEEVE_LOCATION = Pos(0.0, -75.60206157, 81.84312861)


def front_belt_end_sleeve() -> Part:
    return placed(belt_end_sleeve(), FRONT_BELT_END_SLEEVE_LOCATION, "front_belt_end_sleeve")
