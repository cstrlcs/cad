from build123d import Part

from ender3.ender3.reference.components.fan_4010 import fan_4010
from ender3.ender3.reference.construction import placed
from ender3.ender3.reference.electronics.dimensions import CASE_FAN_LOCATION


def case_fan() -> Part:
    return placed(fan_4010(), CASE_FAN_LOCATION, "case_fan")
