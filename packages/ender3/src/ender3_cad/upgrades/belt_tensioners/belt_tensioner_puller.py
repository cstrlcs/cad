from math import sqrt

from bd_warehouse.thread import IsoThread
from build123d import Axis, Cylinder, Part, Plane, Pos, RegularPolygon, Rot, chamfer, extrude

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import BOTTOM, FACE_RIGHT, M5_CLEARANCE_DIAMETER
from ender3_cad.upgrades.belt_tensioners.construction import hole_along_w
from ender3_cad.upgrades.belt_tensioners.dimensions import (
    CASE_END_WALL_INNER_U_ABOVE_TRAVEL_MAX,
    CASE_END_WALL_THICKNESS,
    IDLER_GAP,
    KNOB_HEIGHT,
    M5_NUT_POCKET_DEPTH,
    NUT_POCKET_CLEARANCE,
    PRINTED_THREAD_CLEARANCE,
    PULLER_BRIDGE_END_U,
    PULLER_HALF_HEIGHT,
    PULLER_SLOT_BOTTOM_U,
    PULLER_W_RANGE,
    STEM_MAJOR_DIAMETER,
    STEM_PITCH,
    TENSION_TRAVEL,
)

M5_NUT_ACROSS_FLATS = 8.0

M5_NUT_POCKET_ACROSS_FLATS = M5_NUT_ACROSS_FLATS + NUT_POCKET_CLEARANCE

PULLER_NOSE_WALL = 1.7
PULLER_NOSE_U = -(M5_NUT_POCKET_ACROSS_FLATS / sqrt(3) + PULLER_NOSE_WALL)

STEM_TIP_CHAMFER = 1.0

STEM_TIP_MARGIN = 0.5

PRINT_FROM_NOSE = Rot(0, -90, 0)

PULLER_STEM_TIP_U = (
    CASE_END_WALL_INNER_U_ABOVE_TRAVEL_MAX + TENSION_TRAVEL + CASE_END_WALL_THICKNESS + KNOB_HEIGHT + STEM_TIP_MARGIN
)


def _stem() -> Part:
    length = PULLER_STEM_TIP_U - PULLER_BRIDGE_END_U
    thread = IsoThread(
        major_diameter=STEM_MAJOR_DIAMETER,
        pitch=STEM_PITCH,
        length=length,
        external=True,
        end_finishes=("square", "chamfer"),
        manufacturing_compensation=PRINTED_THREAD_CLEARANCE,
    )
    core = Cylinder(thread.min_radius - PRINTED_THREAD_CLEARANCE, length, align=BOTTOM)
    core = chamfer(core.edges().group_by(Axis.Z)[-1], STEM_TIP_CHAMFER)
    return Pos(PULLER_BRIDGE_END_U, 0, 0) * FACE_RIGHT * (core + thread)


def belt_tensioner_puller() -> Part:
    full_height = (-PULLER_HALF_HEIGHT, PULLER_HALF_HEIGHT)
    puller = block((PULLER_NOSE_U, PULLER_BRIDGE_END_U), PULLER_W_RANGE, full_height)
    puller -= block((PULLER_NOSE_U, PULLER_SLOT_BOTTOM_U), (-IDLER_GAP / 2, IDLER_GAP / 2), full_height)
    puller -= hole_along_w(0, 0, M5_CLEARANCE_DIAMETER, PULLER_W_RANGE)
    nut_pocket = Plane(origin=(0, PULLER_W_RANGE[0], 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0)) * RegularPolygon(
        M5_NUT_POCKET_ACROSS_FLATS / 2, 6, major_radius=False, rotation=30
    )
    puller -= extrude(nut_pocket, M5_NUT_POCKET_DEPTH)
    puller += _stem()
    puller.label = "belt_tensioner_puller"
    puller.color = PRINTED_PART_COLOR
    return puller


def belt_tensioner_puller_for_printing() -> Part:
    return resting_on_bed(PRINT_FROM_NOSE * belt_tensioner_puller())
