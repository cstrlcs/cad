from build123d import Cylinder, Part, Pos, RectangleRounded, extrude

from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.purchased.construction import centered_block

RASPBERRY_PI_CAMERA_PCB_SIZE = (25.0, 23.862)
RASPBERRY_PI_CAMERA_PCB_THICKNESS = 1.12
RASPBERRY_PI_CAMERA_PCB_CORNER_RADIUS = 1.5
RASPBERRY_PI_CAMERA_MOUNTING_HOLE_DIAMETER = 2.2
RASPBERRY_PI_CAMERA_MOUNTING_HOLES = [(2.0, 9.362), (23.0, 9.362), (2.0, 21.862), (23.0, 21.862)]
RASPBERRY_PI_CAMERA_LENS_CENTER = (12.5, 9.462)
RASPBERRY_PI_CAMERA_BLOCK_SIZE = (10.8, 10.8, 3.875)
RASPBERRY_PI_CAMERA_LENS_DIAMETER = 5.75
RASPBERRY_PI_CAMERA_LENS_TIP_HEIGHT = 6.98
RASPBERRY_PI_CAMERA_CONNECTOR_SIZE = (19.61, 5.71, 3.2)


def raspberry_pi_camera_module() -> Part:
    width, height = RASPBERRY_PI_CAMERA_PCB_SIZE
    t = RASPBERRY_PI_CAMERA_PCB_THICKNESS
    pcb = Pos(width / 2, height / 2, -t) * extrude(
        RectangleRounded(width, height, RASPBERRY_PI_CAMERA_PCB_CORNER_RADIUS), t
    ) - [
        Pos(x, y, -t) * Cylinder(RASPBERRY_PI_CAMERA_MOUNTING_HOLE_DIAMETER / 2, t, align=BOTTOM)
        for x, y in RASPBERRY_PI_CAMERA_MOUNTING_HOLES
    ]
    lens_block = centered_block(RASPBERRY_PI_CAMERA_LENS_CENTER, RASPBERRY_PI_CAMERA_BLOCK_SIZE, 0)
    lens = Pos(*RASPBERRY_PI_CAMERA_LENS_CENTER, 0) * Cylinder(
        RASPBERRY_PI_CAMERA_LENS_DIAMETER / 2, RASPBERRY_PI_CAMERA_LENS_TIP_HEIGHT, align=BOTTOM
    )
    connector_width, connector_height, connector_depth = RASPBERRY_PI_CAMERA_CONNECTOR_SIZE
    connector = block(
        (width / 2 - connector_width / 2, width / 2 + connector_width / 2),
        (0, connector_height),
        (-t - connector_depth, -t),
    )
    camera = Part() + [pcb, lens_block, lens, connector]
    camera.label = "raspberry_pi_camera_module"
    return camera
