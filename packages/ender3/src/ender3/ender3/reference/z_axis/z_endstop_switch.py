from build123d import Part, Pos

from ender3.dimensions import FACE_RIGHT
from ender3.ender3.reference.components.limit_switch import limit_switch
from ender3.ender3.reference.construction import placed

Z_ENDSTOP_SWITCH_LOCATION = Pos(-165.0, -31.0, 71.95) * FACE_RIGHT


def z_endstop_switch() -> Part:
    return placed(limit_switch(), Z_ENDSTOP_SWITCH_LOCATION, "z_endstop_switch")
