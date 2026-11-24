from build123d import Part, Plane, mirror

from ender3_cad.construction import ceiling_on_bed
from ender3_cad.upgrades.storage_drawers.construction import labelled, left_storage_housing_body


def right_storage_housing() -> Part:
    return labelled(mirror(left_storage_housing_body(), Plane.YZ), "right_storage_housing")


def right_storage_housing_for_printing() -> Part:
    return ceiling_on_bed(right_storage_housing())
