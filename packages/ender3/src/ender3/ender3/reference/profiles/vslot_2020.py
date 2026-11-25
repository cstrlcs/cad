from build123d import Part, extrude

from ender3.ender3.reference.profiles.construction import vslot_section


def vslot_2020(length: float) -> Part:
    return extrude(vslot_section(1, 1, []), amount=length)
