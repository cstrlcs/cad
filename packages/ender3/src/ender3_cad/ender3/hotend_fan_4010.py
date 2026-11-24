from build123d import Part

from ender3_cad.colors import PURCHASED_PART_COLOR
from ender3_cad.ender3.reference.components.fan_4010 import fan_4010
from ender3_cad.upgrades.fan_duct.dimensions import HOTEND_FAN_LOCATION


def hotend_fan_4010() -> Part:
    fan = HOTEND_FAN_LOCATION * fan_4010()
    fan.label = "hotend_fan_4010"
    fan.color = PURCHASED_PART_COLOR
    return fan
