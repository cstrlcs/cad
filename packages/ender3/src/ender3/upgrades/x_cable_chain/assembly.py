from itertools import pairwise

from build123d import Part

from ender3.upgrades.x_cable_chain.construction import chain_frame, chain_pivots
from ender3.upgrades.x_cable_chain.dimensions import CARRIAGE_PIVOT_X
from ender3.upgrades.x_cable_chain.x_cable_chain_carriage_mount import x_cable_chain_carriage_mount
from ender3.upgrades.x_cable_chain.x_cable_chain_fixed_mount import x_cable_chain_fixed_mount
from ender3.upgrades.x_cable_chain.x_cable_chain_link import x_cable_chain_link
from ender3.upgrades.x_cable_chain.x_cable_chain_link_cover import x_cable_chain_link_cover


def x_cable_chain_parts() -> list[Part]:
    pivots = chain_pivots(CARRIAGE_PIVOT_X)
    link, cover = x_cable_chain_link(), x_cable_chain_link_cover()
    links = []
    for index, (inner, outer) in enumerate(pairwise(pivots), start=1):
        frame = chain_frame(outer, (outer - inner).normalized())
        placed_link, placed_cover = frame * link, frame * cover
        placed_link.label, placed_cover.label = f"x_cable_chain_link_{index}", f"x_cable_chain_link_cover_{index}"
        links += [placed_link, placed_cover]
    return [x_cable_chain_fixed_mount(), *links, x_cable_chain_carriage_mount()]
