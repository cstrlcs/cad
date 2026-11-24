from build123d import Compound

from ender3_cad.ender3.reference.electronics.case_fan import case_fan
from ender3_cad.ender3.reference.electronics.enclosure_bottom_cover import enclosure_bottom_cover
from ender3_cad.ender3.reference.electronics.enclosure_top_cover import enclosure_top_cover
from ender3_cad.ender3.reference.electronics.mainboard import mainboard
from ender3_cad.ender3.reference.electronics.power_supply import power_supply
from ender3_cad.ender3.reference.electronics.power_supply_bracket import power_supply_bracket
from ender3_cad.ender3.reference.electronics.power_switch import power_switch


def electronics() -> Compound:
    return Compound(
        label="electronics",
        children=[
            enclosure_bottom_cover(),
            enclosure_top_cover(),
            mainboard(),
            power_supply(),
            power_supply_bracket(),
            power_switch(),
            case_fan(),
        ],
    )
