from build123d import Part

from ender3_cad.colors import PURCHASED_PART_COLOR
from ender3_cad.ender3.reference.electronics.dimensions import POWER_SUPPLY_LOCATION
from ender3_cad.ender3.reference.electronics.power_supply import power_supply
from ender3_cad.upgrades.power_supply_case.dimensions import PSU_LOCATION


def mean_well_power_supply() -> Part:
    psu = PSU_LOCATION * POWER_SUPPLY_LOCATION.inverse() * power_supply()
    psu.label = "mean_well_power_supply"
    psu.color = PURCHASED_PART_COLOR
    return psu
