from build123d import Part

from ender3.enclosure.panels.construction import bottom_panel


def left_bottom_panel() -> Part:
    return bottom_panel(-1)
