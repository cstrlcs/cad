from build123d import Face, Part, Plane

from ender3_cad.enclosure.dimensions import CLEAR_ACRYLIC_THICKNESS
from ender3_cad.enclosure.panels.dimensions import BLACK_ACRYLIC_THICKNESS
from ender3_cad.enclosure.panels.front_center_plate import front_center_plate
from ender3_cad.enclosure.panels.front_door import front_door
from ender3_cad.enclosure.panels.left_bottom_panel import left_bottom_panel
from ender3_cad.enclosure.panels.left_side_panel import left_side_panel
from ender3_cad.enclosure.panels.rear_center_plate import rear_center_plate
from ender3_cad.enclosure.panels.rear_panel import rear_panel
from ender3_cad.enclosure.panels.right_bottom_panel import right_bottom_panel
from ender3_cad.enclosure.panels.right_side_panel import right_side_panel
from ender3_cad.enclosure.panels.top_panel import top_panel


def laser_cut_outline(part: Part) -> Face:
    face = max(part.faces(), key=lambda f: f.area)
    return Plane(face).to_local_coords(face)


def laser_cut_parts() -> dict[str, Part]:
    sheets = (
        (
            "clear",
            CLEAR_ACRYLIC_THICKNESS,
            (front_door(), rear_panel(), left_side_panel(), right_side_panel(), top_panel()),
        ),
        (
            "black",
            BLACK_ACRYLIC_THICKNESS,
            (left_bottom_panel(), right_bottom_panel(), front_center_plate(), rear_center_plate()),
        ),
    )
    return {f"{material}_{thickness:g}mm_{part.label}": part for material, thickness, parts in sheets for part in parts}
