from build123d import Part, Plane

from ender3.colors import PURCHASED_PART_COLOR
from ender3.enclosure.dimensions import CASE_OUTER_HALF_WIDTH, SWITCH_CENTER_Y, SWITCH_CENTER_Z
from ender3.ender3.reference.electronics.dimensions import POWER_SWITCH_LOCATION
from ender3.ender3.reference.electronics.power_switch import power_switch


def mains_power_switch() -> Part:
    location = Plane(
        origin=(-CASE_OUTER_HALF_WIDTH, SWITCH_CENTER_Y, SWITCH_CENTER_Z), x_dir=(-1, 0, 0), z_dir=(0, 0, 1)
    ).location
    switch = location * POWER_SWITCH_LOCATION.inverse() * power_switch()
    switch.label = "mains_power_switch"
    switch.color = PURCHASED_PART_COLOR
    return switch
