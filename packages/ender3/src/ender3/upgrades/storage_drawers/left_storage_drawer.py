from build123d import Part

from ender3.construction import resting_on_bed
from ender3.upgrades.storage_drawers.construction import labelled, left_storage_drawer_body


def left_storage_drawer() -> Part:
    return labelled(left_storage_drawer_body(), "left_storage_drawer")


def left_storage_drawer_for_printing() -> Part:
    return resting_on_bed(left_storage_drawer())
