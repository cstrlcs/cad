from pathlib import Path

from build123d import Compound, Pos, export_stl
from ocp_vscode import show

from gridfinity.baseplate import baseplate
from gridfinity.bins import gridfinity_bin
from gridfinity.hardware_box import closed_lid_location, hardware_box, hardware_box_lid
from gridfinity.spec import BIN_GAP, GRID_PITCH

STL_DIR = Path("stl")


def main() -> None:
    divider_bin_units = (2, 2, 6)
    box_units = (4, 3, 3)
    plate = baseplate(5, 5)
    divider_bin = gridfinity_bin(*divider_bin_units, compartments_x=3, compartments_y=3)
    screw_box = hardware_box(*box_units)
    screw_box_lid = hardware_box_lid(*box_units)
    STL_DIR.mkdir(exist_ok=True)
    for part in (plate, divider_bin, screw_box, screw_box_lid):
        export_stl(part, STL_DIR / f"gridfinity_{part.label}.stl")
    bin_seat = Pos(BIN_GAP / 2, BIN_GAP / 2, 0)
    box_seat = Pos(0, divider_bin_units[1] * GRID_PITCH, 0) * bin_seat
    show(
        Compound(
            label="gridfinity",
            children=[
                plate,
                bin_seat * divider_bin,
                box_seat * screw_box,
                box_seat * closed_lid_location(*box_units) * screw_box_lid,
            ],
        )
    )
