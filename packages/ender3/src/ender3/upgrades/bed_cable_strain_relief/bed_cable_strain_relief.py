from build123d import Cylinder, Part, Pos

from ender3.colors import PRINTED_PART_COLOR
from ender3.construction import block, resting_on_bed
from ender3.dimensions import BOTTOM, FACE_DOWN
from ender3.ender3.reference.y_axis.dimensions import BED_BOTTOM_Z, BED_LEVELING_HOLE_POSITIONS
from ender3.upgrades.bed_cable_strain_relief.dimensions import CABLE_X, POST_BACK_Y, POST_BOTTOM_Z, POST_FRONT_Y

REAR_LEFT_LEVELING_HOLE = 3
LEVELING_SCREW_X, LEVELING_SCREW_Y = BED_LEVELING_HOLE_POSITIONS[REAR_LEFT_LEVELING_HOLE]

LEVELING_SCREW_CLEARANCE_DIAMETER = 4.6
PLATE_THICKNESS = 3.0
RING_DIAMETER = 11.0
ARM_WIDTH = 12.0

GUIDE_WALL = 1.6

GUIDE_DEPTH = 4.0
ZIP_TIE_SLOT_HEIGHT = 4.0
ZIP_TIE_SLOT_DEPTH = 2.4
ZIP_TIE_SLOT_END_INSET = 4.0
ZIP_TIE_SLOT_CENTERS_Z = (
    BED_BOTTOM_Z - PLATE_THICKNESS - ZIP_TIE_SLOT_END_INSET,
    POST_BOTTOM_Z + ZIP_TIE_SLOT_END_INSET,
)


def bed_cable_strain_relief() -> Part:
    arm_x = (CABLE_X - ARM_WIDTH / 2, CABLE_X + ARM_WIDTH / 2)
    plate_z = (BED_BOTTOM_Z - PLATE_THICKNESS, BED_BOTTOM_Z)
    ring = Pos(LEVELING_SCREW_X, LEVELING_SCREW_Y, plate_z[0]) * Cylinder(
        RING_DIAMETER / 2, PLATE_THICKNESS, align=BOTTOM
    )
    arm = block(arm_x, (LEVELING_SCREW_Y, POST_BACK_Y), plate_z)
    post = block(arm_x, (POST_FRONT_Y, POST_BACK_Y), (POST_BOTTOM_Z, plate_z[1]))
    guides = [
        block(x_range, (POST_BACK_Y, POST_BACK_Y + GUIDE_DEPTH), (POST_BOTTOM_Z, plate_z[0]))
        for x_range in [(arm_x[0], arm_x[0] + GUIDE_WALL), (arm_x[1] - GUIDE_WALL, arm_x[1])]
    ]
    screw_hole = Pos(LEVELING_SCREW_X, LEVELING_SCREW_Y, plate_z[0]) * Cylinder(
        LEVELING_SCREW_CLEARANCE_DIAMETER / 2, PLATE_THICKNESS, align=BOTTOM
    )
    slot_y = (
        (POST_FRONT_Y + POST_BACK_Y - ZIP_TIE_SLOT_DEPTH) / 2,
        (POST_FRONT_Y + POST_BACK_Y + ZIP_TIE_SLOT_DEPTH) / 2,
    )
    zip_tie_slots = [
        block(arm_x, slot_y, (z - ZIP_TIE_SLOT_HEIGHT / 2, z + ZIP_TIE_SLOT_HEIGHT / 2)) for z in ZIP_TIE_SLOT_CENTERS_Z
    ]
    relief = ring + arm + post + guides - screw_hole - zip_tie_slots
    relief.label = "bed_cable_strain_relief"
    relief.color = PRINTED_PART_COLOR
    return relief


def bed_cable_strain_relief_for_printing() -> Part:
    return resting_on_bed(FACE_DOWN * bed_cable_strain_relief())
