from build123d import Part, Vector

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import M3_HEAT_SET_INSERT_DEPTH, M3_HEAT_SET_INSERT_HOLE_DIAMETER
from ender3.enclosure.accessories.construction import hinge_knuckle_ranges, hinge_z_range, knuckled_leaf
from ender3.enclosure.accessories.dimensions import HINGE_LEAF_LENGTH, HINGE_LEAF_THICKNESS
from ender3.enclosure.construction import blind_hole, frame_hinge_screw_points
from ender3.enclosure.dimensions import CASE_OUTER_HALF_WIDTH, HINGE_AXIS, HINGE_CENTERS_Z


def hinge_frame_leaf(index: int) -> Part:
    center_z = HINGE_CENTERS_Z[index]
    bottom, middle, top = hinge_knuckle_ranges(center_z)
    plate = block(
        (-CASE_OUTER_HALF_WIDTH - HINGE_LEAF_THICKNESS, -CASE_OUTER_HALF_WIDTH),
        (HINGE_AXIS.Y, HINGE_AXIS.Y + HINGE_LEAF_LENGTH),
        hinge_z_range(center_z),
    )
    leaf = knuckled_leaf(plate, center_z, own=(bottom, top), other=(middle,))
    leaf -= [
        blind_hole(point, Vector(-1, 0, 0), M3_HEAT_SET_INSERT_HOLE_DIAMETER, M3_HEAT_SET_INSERT_DEPTH)
        for point in frame_hinge_screw_points(center_z)
    ]
    leaf.label = f"hinge_frame_leaf_{index + 1}"
    leaf.color = PRINTED_PART_COLOR
    return leaf


def hinge_frame_leaf_for_printing() -> Part:
    return resting_on_bed(hinge_frame_leaf(0))
