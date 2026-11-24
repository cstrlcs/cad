from build123d import Location, Part

from ender3_cad.ender3.reference.components.limit_switch import limit_switch
from ender3_cad.ender3.reference.construction import placed
from ender3_cad.ender3.reference.x_axis.dimensions import X_BEAM_AXIS_Z

X_ENDSTOP_SWITCH_LOCATION = Location((-176.65, -46.75, X_BEAM_AXIS_Z), (90, 0, -180))


def x_endstop_switch() -> Part:
    return placed(limit_switch(), X_ENDSTOP_SWITCH_LOCATION, "x_endstop_switch")
