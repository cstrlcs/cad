from build123d import Part, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3.enclosure.accessories.construction import hinge_knuckle_ranges, hinge_z_range, knuckled_leaf
from ender3.enclosure.accessories.dimensions import HINGE_LEAF_LENGTH, HINGE_LEAF_THICKNESS
from ender3.enclosure.construction import blind_hole, door_hinge_screw_points
from ender3.enclosure.dimensions import DOOR_FRONT_Y, HINGE_AXIS, HINGE_CENTERS_Z


def hinge_door_leaf(index: int) -> Part:
    center_z = HINGE_CENTERS_Z[index]
    bottom, middle, top = hinge_knuckle_ranges(center_z)
    plate = block(
        (HINGE_AXIS.X, HINGE_AXIS.X + HINGE_LEAF_LENGTH),
        (DOOR_FRONT_Y - HINGE_LEAF_THICKNESS, DOOR_FRONT_Y),
        hinge_z_range(center_z),
    )
    leaf = knuckled_leaf(plate, center_z, own=(middle,), other=(bottom, top))
    leaf -= [
        blind_hole(point, Vector(0, -1, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH)
        for point in door_hinge_screw_points(center_z)
    ]
    leaf.label = f"hinge_door_leaf_{index + 1}"
    leaf.color = PRINTED_PART_COLOR
    return leaf


def hinge_door_leaf_for_printing() -> Part:
    return resting_on_bed(hinge_door_leaf(0))
