from build123d import Location, Part

from ender3.ender3.reference.components.limit_switch import limit_switch
from ender3.ender3.reference.construction import placed

Y_ENDSTOP_SWITCH_LOCATION = Location((25.0, 114.05, 58.21295), (0, 90, 90))


def y_endstop_switch() -> Part:
    return placed(limit_switch(), Y_ENDSTOP_SWITCH_LOCATION, "y_endstop_switch")
