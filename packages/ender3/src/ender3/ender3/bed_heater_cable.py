from build123d import Circle, FilletPolyline, Part, Plane, sweep

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.reference.y_axis.dimensions import BED_BOTTOM_Z, BED_CENTER_Y, BED_HEATER_PAD_POCKET_CENTER
from ender3.upgrades.bed_cable_strain_relief.dimensions import CABLE_X, POST_BACK_Y, POST_BOTTOM_Z

PAD_CENTER_Y = BED_CENTER_Y + BED_HEATER_PAD_POCKET_CENTER[1]

CABLE_DIAMETER = 8.0

CABLE_BEND_RADIUS = 6.0
CABLE_DROP_BELOW_POST = 10.0


def bed_heater_cable() -> Part:
    cable_y = POST_BACK_Y + CABLE_DIAMETER / 2
    top_z = BED_BOTTOM_Z - CABLE_DIAMETER / 2
    start = (CABLE_X, PAD_CENTER_Y + CABLE_DIAMETER / 2, top_z)
    path = FilletPolyline(
        start,
        (CABLE_X, cable_y, top_z),
        (CABLE_X, cable_y, POST_BOTTOM_Z - CABLE_DROP_BELOW_POST),
        radius=CABLE_BEND_RADIUS,
    )
    cable = sweep(Plane(origin=start, z_dir=(0, -1, 0)) * Circle(CABLE_DIAMETER / 2), path)
    cable.label = "bed_heater_cable"
    cable.color = PURCHASED_PART_COLOR
    return cable
