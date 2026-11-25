from build123d import Part

from ender3.colors import PURCHASED_PART_COLOR
from ender3.enclosure.construction import camera_location
from ender3.ender3.purchased.raspberry_pi_camera_module import raspberry_pi_camera_module


def raspberry_pi_camera() -> Part:
    camera = camera_location() * raspberry_pi_camera_module()
    camera.label = "raspberry_pi_camera"
    camera.color = PURCHASED_PART_COLOR
    return camera
