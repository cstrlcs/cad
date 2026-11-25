from build123d import Part, Plane, mirror

from ender3.construction import resting_on_bed
from ender3.upgrades.storage_drawers.construction import labelled, left_storage_drawer_body


def right_storage_drawer() -> Part:
    return labelled(mirror(left_storage_drawer_body(), Plane.YZ), "right_storage_drawer")


def right_storage_drawer_for_printing() -> Part:
    return resting_on_bed(right_storage_drawer())
