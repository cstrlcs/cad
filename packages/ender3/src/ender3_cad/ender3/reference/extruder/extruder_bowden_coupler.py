from build123d import Axis, Part, Plane, Pos, RegularPolygon, extrude, fillet

from ender3_cad.dimensions import CUT_OVERSHOOT
from ender3_cad.ender3.reference.extruder.construction import x_cylinder
from ender3_cad.ender3.reference.extruder.dimensions import (
    EXTRUDER_MOUNT_LOCATION,
    FILAMENT_PATH_LOCAL_YZ,
    HOUSING_FRONT_X,
)

COUPLER_STEM_X_RANGE = (16.0275, HOUSING_FRONT_X)
COUPLER_STEM_DIAMETER = 6.0
COUPLER_HEX_X_RANGE = (HOUSING_FRONT_X, 26.0275)
COUPLER_HEX_ACROSS_FLATS = 8.0
COUPLER_HEX_ROTATION = 11.2758
COUPLER_COLLET_X_RANGE = (26.0275, 31.0275)
COUPLER_COLLET_DIAMETER = 8.0
COUPLER_COLLET_GROOVE_X_RANGE = (28.4839, 29.4674)
COUPLER_COLLET_GROOVE_DIAMETER = 5.791
COUPLER_COLLET_EDGE_RADIUS = 0.5
COUPLER_BORE_DIAMETER = 3.2


def extruder_bowden_coupler() -> Part:
    stem_start, stem_end = COUPLER_STEM_X_RANGE
    coupler = x_cylinder(COUPLER_STEM_DIAMETER, stem_start, stem_end, *FILAMENT_PATH_LOCAL_YZ)
    hex_start, hex_end = COUPLER_HEX_X_RANGE
    coupler += extrude(
        Plane.YZ.offset(hex_start)
        * Pos(*FILAMENT_PATH_LOCAL_YZ)
        * RegularPolygon(
            COUPLER_HEX_ACROSS_FLATS / 2,
            6,
            major_radius=False,
            rotation=COUPLER_HEX_ROTATION,
        ),
        hex_end - hex_start,
    )
    collet_start, collet_end = COUPLER_COLLET_X_RANGE
    collet = x_cylinder(COUPLER_COLLET_DIAMETER, collet_start, collet_end, *FILAMENT_PATH_LOCAL_YZ)
    collet = fillet(collet.edges().group_by(Axis.X)[-1], COUPLER_COLLET_EDGE_RADIUS)
    groove_start, groove_end = COUPLER_COLLET_GROOVE_X_RANGE
    collet -= x_cylinder(
        COUPLER_COLLET_DIAMETER + CUT_OVERSHOOT,
        groove_start,
        groove_end,
        *FILAMENT_PATH_LOCAL_YZ,
    ) - x_cylinder(
        COUPLER_COLLET_GROOVE_DIAMETER,
        groove_start,
        groove_end,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    coupler += collet
    coupler -= x_cylinder(
        COUPLER_BORE_DIAMETER,
        stem_start - CUT_OVERSHOOT,
        hex_start,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    coupler -= x_cylinder(
        COUPLER_BORE_DIAMETER,
        hex_end,
        collet_end + CUT_OVERSHOOT,
        *FILAMENT_PATH_LOCAL_YZ,
    )
    coupler = EXTRUDER_MOUNT_LOCATION * coupler
    coupler.label = "extruder_bowden_coupler"
    return coupler
