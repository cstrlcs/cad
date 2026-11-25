from build123d import Keep, Part

from ender3.construction import ceiling_on_bed
from ender3.upgrades.power_supply_case.construction import power_supply_drawer_half


def right_power_supply_drawer() -> Part:
    return power_supply_drawer_half(Keep.TOP, "right_power_supply_drawer")


def right_power_supply_drawer_for_printing() -> Part:
    return ceiling_on_bed(right_power_supply_drawer())
