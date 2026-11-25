from build123d import Part, Pos

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.reference.components.fan_4010 import fan_4010
from ender3.upgrades.board_cases.dimensions import RIGHT_FAN_CENTER, TRAY_TOP_Z


def right_drawer_fan() -> Part:
    fan = Pos(*RIGHT_FAN_CENTER, TRAY_TOP_Z) * fan_4010()
    fan.label = "right_drawer_fan"
    fan.color = PURCHASED_PART_COLOR
    return fan
