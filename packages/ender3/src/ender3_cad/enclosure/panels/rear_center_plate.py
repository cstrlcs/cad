from build123d import Part

from ender3_cad.enclosure.panels.construction import acrylic_panel, center_plate
from ender3_cad.enclosure.panels.dimensions import BLACK_ACRYLIC_COLOR, CENTER_PLATE_SIDE_GAP
from ender3_cad.ender3.reference.frame.dimensions import CROSS_MEMBER_LOCATION, PROFILE_4040_HALF_SIZE
from ender3_cad.upgrades.board_cases.dimensions import LEFT_INNER_X, PANEL_FRONT_Y

CENTER_PLATE_CROSS_MEMBER_GAP = 0.5
CENTER_PLATE_BACK_Y = CROSS_MEMBER_LOCATION.position.Y - PROFILE_4040_HALF_SIZE - CENTER_PLATE_CROSS_MEMBER_GAP
CENTER_PLATE_REAR_HALF_WIDTH = -LEFT_INNER_X - CENTER_PLATE_SIDE_GAP

CENTER_PLATE_REAR_SCREW_Y = (-130.0, -60.0)


def rear_center_plate() -> Part:
    plate = center_plate(CENTER_PLATE_REAR_HALF_WIDTH, (PANEL_FRONT_Y, CENTER_PLATE_BACK_Y), CENTER_PLATE_REAR_SCREW_Y)
    return acrylic_panel(plate, "rear_center_plate", BLACK_ACRYLIC_COLOR)
