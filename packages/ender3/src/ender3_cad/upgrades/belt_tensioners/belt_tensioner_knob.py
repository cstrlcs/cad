from bd_warehouse.thread import IsoThread
from build123d import Cylinder, Part, chamfer

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.dimensions import BOTTOM
from ender3_cad.upgrades.belt_tensioners.dimensions import (
    KNOB_HEIGHT,
    PRINTED_THREAD_CLEARANCE,
    STEM_MAJOR_DIAMETER,
    STEM_PITCH,
)

KNOB_DIAMETER = 32.0

KNOB_EDGE_CHAMFER = 1.0


def belt_tensioner_knob() -> Part:
    knob = Cylinder(KNOB_DIAMETER / 2, KNOB_HEIGHT, align=BOTTOM)
    knob = chamfer(knob.edges(), KNOB_EDGE_CHAMFER)
    knob -= Cylinder(STEM_MAJOR_DIAMETER / 2 + PRINTED_THREAD_CLEARANCE, KNOB_HEIGHT, align=BOTTOM)
    knob += IsoThread(
        major_diameter=STEM_MAJOR_DIAMETER,
        pitch=STEM_PITCH,
        length=KNOB_HEIGHT,
        external=False,
        end_finishes=("chamfer", "chamfer"),
        manufacturing_compensation=PRINTED_THREAD_CLEARANCE,
    )
    knob.label = "belt_tensioner_knob"
    knob.color = PRINTED_PART_COLOR
    return knob
