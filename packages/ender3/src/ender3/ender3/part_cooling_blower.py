from build123d import Part, Plane

from ender3.colors import PURCHASED_PART_COLOR
from ender3.ender3.purchased.blower_5015 import blower_5015
from ender3.upgrades.fan_duct.dimensions import BLOWER_FACE_DOWN, FLANGE_PLANE, SOCKET_DEPTH


def part_cooling_blower() -> Part:
    location = Plane(
        origin=FLANGE_PLANE.from_local_coords((0, BLOWER_FACE_DOWN, SOCKET_DEPTH)),
        x_dir=FLANGE_PLANE.x_dir,
        z_dir=FLANGE_PLANE.y_dir,
    ).location
    blower = location * blower_5015()
    blower.label = "part_cooling_blower"
    blower.color = PURCHASED_PART_COLOR
    return blower
