from build123d import Cylinder, Part, Pos

from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.purchased.construction import centered_block

LM2596_PCB_SIZE = (43.0, 21.0)
LM2596_PCB_THICKNESS = 1.35
LM2596_MOUNTING_HOLE_DIAMETER = 3.0
LM2596_MOUNTING_HOLES = [(7.0, 2.29), (36.0, 18.71)]
LM2596_CAPACITOR_DIAMETER = 10.0
LM2596_CAPACITOR_HEIGHT = 10.6
LM2596_CAPACITOR_CENTERS = [(5.1, 10.4), (37.9, 10.4)]
LM2596_INDUCTOR_CENTER = (16.45, 6.2)
LM2596_INDUCTOR_SIZE = (12.3, 12.3, 7.2)
LM2596_REGULATOR_CENTER = (27.75, 12.36)
LM2596_REGULATOR_SIZE = (10.2, 14.35, 4.6)
LM2596_POTENTIOMETER_CENTER = (10.47, 18.59)
LM2596_POTENTIOMETER_SIZE = (9.5, 4.8, 11.55)


def lm2596_module() -> Part:
    length, width = LM2596_PCB_SIZE
    t = LM2596_PCB_THICKNESS
    pcb = block((0, length), (0, width), (0, t)) - [
        Pos(x, y, 0) * Cylinder(LM2596_MOUNTING_HOLE_DIAMETER / 2, t, align=BOTTOM) for x, y in LM2596_MOUNTING_HOLES
    ]
    capacitors = [
        Pos(x, y, t) * Cylinder(LM2596_CAPACITOR_DIAMETER / 2, LM2596_CAPACITOR_HEIGHT, align=BOTTOM)
        for x, y in LM2596_CAPACITOR_CENTERS
    ]
    inductor = centered_block(LM2596_INDUCTOR_CENTER, LM2596_INDUCTOR_SIZE, t)
    regulator = centered_block(LM2596_REGULATOR_CENTER, LM2596_REGULATOR_SIZE, t)
    potentiometer = centered_block(LM2596_POTENTIOMETER_CENTER, LM2596_POTENTIOMETER_SIZE, t)
    module = Part() + [pcb, *capacitors, inductor, regulator, potentiometer]
    module.label = "lm2596_module"
    return module
