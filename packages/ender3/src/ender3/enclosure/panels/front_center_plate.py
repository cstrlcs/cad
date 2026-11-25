from build123d import Part

from ender3.enclosure.dimensions import DOOR_BACK_Y, DRAWER_FRONT_INNER_X
from ender3.enclosure.panels.construction import acrylic_panel, center_plate
from ender3.enclosure.panels.dimensions import BLACK_ACRYLIC_COLOR, CENTER_PLATE_SIDE_GAP
from ender3.upgrades.board_cases.dimensions import PANEL_FRONT_Y

CENTER_PLATE_FRONT_HALF_WIDTH = -DRAWER_FRONT_INNER_X - CENTER_PLATE_SIDE_GAP

CENTER_PLATE_FRONT_SCREW_Y = (-215.0, -175.0)


def front_center_plate() -> Part:
    plate = center_plate(CENTER_PLATE_FRONT_HALF_WIDTH, (DOOR_BACK_Y, PANEL_FRONT_Y), CENTER_PLATE_FRONT_SCREW_Y)
    return acrylic_panel(plate, "front_center_plate", BLACK_ACRYLIC_COLOR)
