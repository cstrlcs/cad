from build123d import Cylinder, Part, Pos, RectangleRounded, extrude

from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM
from ender3_cad.ender3.purchased.construction import centered_block

RASPBERRY_PI_3B_PCB_SIZE = (85.0, 56.0)
RASPBERRY_PI_3B_PCB_THICKNESS = 1.4
RASPBERRY_PI_3B_PCB_CORNER_RADIUS = 3.0
RASPBERRY_PI_3B_MOUNTING_HOLE_DIAMETER = 2.75
RASPBERRY_PI_3B_MOUNTING_HOLES = [(3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)]
RASPBERRY_PI_3B_USB_X = (69.6, 87.1)
RASPBERRY_PI_3B_USB_WIDTH = 13.2
RASPBERRY_PI_3B_USB_HEIGHT = 16.0
RASPBERRY_PI_3B_USB_CENTERS_Y = (29.0, 47.0)
RASPBERRY_PI_3B_ETHERNET_X = (65.6, 87.1)
RASPBERRY_PI_3B_ETHERNET_WIDTH = 16.0
RASPBERRY_PI_3B_ETHERNET_HEIGHT = 13.5
RASPBERRY_PI_3B_ETHERNET_CENTER_Y = 10.25
RASPBERRY_PI_3B_MICRO_USB_CENTER_X = 10.6
RASPBERRY_PI_3B_MICRO_USB_WIDTH = 8.0
RASPBERRY_PI_3B_MICRO_USB_Y = (-1.0, 4.6)
RASPBERRY_PI_3B_MICRO_USB_HEIGHT = 3.0
RASPBERRY_PI_3B_HDMI_CENTER_X = 32.0
RASPBERRY_PI_3B_HDMI_WIDTH = 15.0
RASPBERRY_PI_3B_HDMI_Y = (-1.0, 10.5)
RASPBERRY_PI_3B_HDMI_HEIGHT = 6.5
RASPBERRY_PI_3B_AUDIO_CENTER_X = 53.5
RASPBERRY_PI_3B_AUDIO_WIDTH = 7.0
RASPBERRY_PI_3B_AUDIO_Y = (-2.5, 12.5)
RASPBERRY_PI_3B_CAMERA_CONNECTOR_CENTER = (45.0, 11.5)
RASPBERRY_PI_3B_AUDIO_HEIGHT = 6.0
RASPBERRY_PI_3B_GPIO_CENTER = (32.5, 52.5)
RASPBERRY_PI_3B_GPIO_SIZE = (50.8, 5.1)
RASPBERRY_PI_3B_GPIO_HEIGHT = 8.5
RASPBERRY_PI_3B_SOC_CENTER = (26.4, 31.8)
RASPBERRY_PI_3B_SOC_SIZE = 14.0
RASPBERRY_PI_3B_SOC_HEIGHT = 1.2
RASPBERRY_PI_3B_MICRO_SD_X = (-2.5, 11.5)
RASPBERRY_PI_3B_MICRO_SD_WIDTH = 12.0
RASPBERRY_PI_3B_MICRO_SD_CENTER_Y = 28.0
RASPBERRY_PI_3B_MICRO_SD_HEIGHT = 1.5


def raspberry_pi_3b() -> Part:
    length, width = RASPBERRY_PI_3B_PCB_SIZE
    t = RASPBERRY_PI_3B_PCB_THICKNESS
    pcb = Pos(length / 2, width / 2) * extrude(
        RectangleRounded(length, width, RASPBERRY_PI_3B_PCB_CORNER_RADIUS), t
    ) - [
        Pos(x, y, 0) * Cylinder(RASPBERRY_PI_3B_MOUNTING_HOLE_DIAMETER / 2, t, align=BOTTOM)
        for x, y in RASPBERRY_PI_3B_MOUNTING_HOLES
    ]
    usb_stacks = [
        block(
            RASPBERRY_PI_3B_USB_X,
            (y - RASPBERRY_PI_3B_USB_WIDTH / 2, y + RASPBERRY_PI_3B_USB_WIDTH / 2),
            (t, t + RASPBERRY_PI_3B_USB_HEIGHT),
        )
        for y in RASPBERRY_PI_3B_USB_CENTERS_Y
    ]
    ethernet = block(
        RASPBERRY_PI_3B_ETHERNET_X,
        (
            RASPBERRY_PI_3B_ETHERNET_CENTER_Y - RASPBERRY_PI_3B_ETHERNET_WIDTH / 2,
            RASPBERRY_PI_3B_ETHERNET_CENTER_Y + RASPBERRY_PI_3B_ETHERNET_WIDTH / 2,
        ),
        (t, t + RASPBERRY_PI_3B_ETHERNET_HEIGHT),
    )
    side_ports = [
        block((center_x - port_width / 2, center_x + port_width / 2), port_y, (t, t + port_height))
        for center_x, port_width, port_y, port_height in (
            (
                RASPBERRY_PI_3B_MICRO_USB_CENTER_X,
                RASPBERRY_PI_3B_MICRO_USB_WIDTH,
                RASPBERRY_PI_3B_MICRO_USB_Y,
                RASPBERRY_PI_3B_MICRO_USB_HEIGHT,
            ),
            (
                RASPBERRY_PI_3B_HDMI_CENTER_X,
                RASPBERRY_PI_3B_HDMI_WIDTH,
                RASPBERRY_PI_3B_HDMI_Y,
                RASPBERRY_PI_3B_HDMI_HEIGHT,
            ),
            (
                RASPBERRY_PI_3B_AUDIO_CENTER_X,
                RASPBERRY_PI_3B_AUDIO_WIDTH,
                RASPBERRY_PI_3B_AUDIO_Y,
                RASPBERRY_PI_3B_AUDIO_HEIGHT,
            ),
        )
    ]
    gpio_header = centered_block(
        RASPBERRY_PI_3B_GPIO_CENTER, (*RASPBERRY_PI_3B_GPIO_SIZE, RASPBERRY_PI_3B_GPIO_HEIGHT), t
    )
    soc = centered_block(
        RASPBERRY_PI_3B_SOC_CENTER, (RASPBERRY_PI_3B_SOC_SIZE, RASPBERRY_PI_3B_SOC_SIZE, RASPBERRY_PI_3B_SOC_HEIGHT), t
    )
    micro_sd = block(
        RASPBERRY_PI_3B_MICRO_SD_X,
        (
            RASPBERRY_PI_3B_MICRO_SD_CENTER_Y - RASPBERRY_PI_3B_MICRO_SD_WIDTH / 2,
            RASPBERRY_PI_3B_MICRO_SD_CENTER_Y + RASPBERRY_PI_3B_MICRO_SD_WIDTH / 2,
        ),
        (-RASPBERRY_PI_3B_MICRO_SD_HEIGHT, 0),
    )
    pi = Part() + [pcb, *usb_stacks, ethernet, *side_ports, gpio_header, soc, micro_sd]
    pi.label = "raspberry_pi_3b"
    return pi
