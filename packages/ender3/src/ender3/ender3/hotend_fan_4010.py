from build123d import Part

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.reference.components.fan_4010 import fan_4010
from ender3.upgrades.fan_duct.dimensions import HOTEND_FAN_LOCATION


def hotend_fan_4010() -> Part:
    fan = HOTEND_FAN_LOCATION * fan_4010()
    fan.label = "hotend_fan_4010"
    fan.color = PURCHASED_PART_COLOR
    return fan
