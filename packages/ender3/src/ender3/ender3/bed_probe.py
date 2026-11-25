from build123d import Part, Pos

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.purchased.cr_touch import CR_TOUCH_BODY_WIDTH, CR_TOUCH_MOUNT_TO_PIN_TIP, cr_touch
from ender3.ender3.reference.print_head.dimensions import HOTEND_AXIS_X
from ender3.upgrades.fan_duct.dimensions import ARM_SIDE_X_OFFSET, ARM_SIZE, MEASURED_NOZZLE_TIP_Z

PROBE_CLEARANCE_TO_DUCT_ARM = 0.5
PROBE_AXIS_X = HOTEND_AXIS_X - ARM_SIDE_X_OFFSET - ARM_SIZE / 2 - PROBE_CLEARANCE_TO_DUCT_ARM - CR_TOUCH_BODY_WIDTH / 2
PROBE_AXIS_Y = -69.5
PROBE_RETRACTED_PIN_ABOVE_NOZZLE_TIP = 3.0
PROBE_MOUNT_FACE_Z = MEASURED_NOZZLE_TIP_Z + PROBE_RETRACTED_PIN_ABOVE_NOZZLE_TIP + CR_TOUCH_MOUNT_TO_PIN_TIP


def bed_probe() -> Part:
    probe = Pos(PROBE_AXIS_X, PROBE_AXIS_Y, PROBE_MOUNT_FACE_Z) * cr_touch()
    probe.label = "bed_probe"
    probe.color = PURCHASED_PART_COLOR
    return probe
