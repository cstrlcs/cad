from build123d import Part

from ender3.construction import ceiling_on_bed
from ender3.upgrades.storage_drawers.construction import labelled, left_storage_housing_body


def left_storage_housing() -> Part:
    return labelled(left_storage_housing_body(), "left_storage_housing")


def left_storage_housing_for_printing() -> Part:
    return ceiling_on_bed(left_storage_housing())
