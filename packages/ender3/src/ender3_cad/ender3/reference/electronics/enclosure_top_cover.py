from build123d import Axis, Part, Plane, Pos, extrude, fillet

from ender3_cad.construction import block
from ender3_cad.dimensions import CUT_OVERSHOOT, FACE_BACK
from ender3_cad.ender3.reference.construction import outline_face, range_rectangle
from ender3_cad.ender3.reference.electronics.construction import thin_plate_hole
from ender3_cad.ender3.reference.electronics.dimensions import (
    ENCLOSURE_CORNER_RADIUS,
    ENCLOSURE_LOCATION,
    ENCLOSURE_SCREW_HOLE_DIAMETER,
    ENCLOSURE_SHEET_THICKNESS,
    TOP_COVER_FRAME_SCREW_HOLES,
)

TOP_COVER_PLATE_X_RANGE = (0.0, 104.0)
TOP_COVER_PLATE_Y_RANGE = (-1.0, 164.0)
TOP_COVER_PLATE_Z_RANGE = (40.0, 41.0)
TOP_COVER_BEND_OUTER_RADIUS = 1.0
TOP_COVER_PLATE_NOTCH_X = 4.0
TOP_COVER_PLATE_NOTCH_START_Y = 118.0
TOP_COVER_PLATE_SCREW_HOLES = [(65.0, 134.0), (99.0, 55.0)]
TOP_COVER_FRONT_PLATE_X_RANGE = (-39.0, 104.0)
TOP_COVER_FRONT_PLATE_Z_RANGE = (-1.0, 40.0)
TOP_COVER_TAB_X_RANGES = [(3.0, 15.0), (89.0, 101.0)]
TOP_COVER_TAB_LENGTH = 9.0
TOP_COVER_TAB_RELIEF_WIDTH = 0.5
TOP_COVER_TAB_RELIEF_TOP = 1.5
TOP_COVER_TAB_SCREW_HOLES = [(9.0, 4.0), (95.0, 4.0)]
TOP_COVER_FRAME_SCREW_HOLE_DIAMETER = 5.2

SD_CARD_SLOT_X_RANGE = (18.0, 34.0)
SD_CARD_SLOT_Z_RANGE = (32.0, 34.0)
USB_PORT_OPENING_X_RANGE = (38.0, 46.0)
USB_PORT_OPENING_Z_RANGE = (30.0, 34.5)


def enclosure_top_cover() -> Part:
    t = ENCLOSURE_SHEET_THICKNESS
    radius = ENCLOSURE_CORNER_RADIUS
    (px0, px1), (py0, py1), (pz0, pz1) = TOP_COVER_PLATE_X_RANGE, TOP_COVER_PLATE_Y_RANGE, TOP_COVER_PLATE_Z_RANGE
    notch_x = px0 + TOP_COVER_PLATE_NOTCH_X
    plate_outline = outline_face(
        [
            (px0, py0),
            (px1, py0),
            (px1, py1),
            (notch_x, py1),
            (notch_x, TOP_COVER_PLATE_NOTCH_START_Y),
            (px0, TOP_COVER_PLATE_NOTCH_START_Y),
        ],
        [0, 0, radius, radius, radius, radius],
    )
    plate = Pos(0, 0, pz0) * extrude(plate_outline, pz1 - pz0)
    (fx0, fx1), (fz0, fz1) = TOP_COVER_FRONT_PLATE_X_RANGE, TOP_COVER_FRONT_PLATE_Z_RANGE
    front_outline = outline_face([(fx0, fz0), (fx1, fz0), (fx1, fz1), (fx0, fz1)], [radius, radius, 0, radius])
    reliefs = [
        range_rectangle(
            (x0 - TOP_COVER_TAB_RELIEF_WIDTH, x1 + TOP_COVER_TAB_RELIEF_WIDTH),
            (fz0 - CUT_OVERSHOOT, TOP_COVER_TAB_RELIEF_TOP),
        )
        for x0, x1 in TOP_COVER_TAB_X_RANGES
    ]
    front = extrude(Plane.XZ.offset(-py0) * (front_outline - reliefs), -t)
    tabs = [
        extrude(
            outline_face(
                [(x0, py0), (x1, py0), (x1, TOP_COVER_TAB_LENGTH), (x0, TOP_COVER_TAB_LENGTH)],
                [0, 0, radius, radius],
            ),
            t,
        )
        + block((x0, x1), (py0, py0 + t), (0, TOP_COVER_TAB_RELIEF_TOP))
        for x0, x1 in TOP_COVER_TAB_X_RANGES
    ]
    plate_holes = [
        Pos(x, y, pz0) * thin_plate_hole(ENCLOSURE_SCREW_HOLE_DIAMETER) for x, y in TOP_COVER_PLATE_SCREW_HOLES
    ]
    tab_holes = [Pos(x, y, 0) * thin_plate_hole(ENCLOSURE_SCREW_HOLE_DIAMETER) for x, y in TOP_COVER_TAB_SCREW_HOLES]
    frame_holes = [
        Pos(x, py0, z) * FACE_BACK * thin_plate_hole(TOP_COVER_FRAME_SCREW_HOLE_DIAMETER)
        for x, z in TOP_COVER_FRAME_SCREW_HOLES
    ]
    port_y_range = (py0 - CUT_OVERSHOOT, py0 + t + CUT_OVERSHOOT)
    port_openings = [
        block(SD_CARD_SLOT_X_RANGE, port_y_range, SD_CARD_SLOT_Z_RANGE),
        block(USB_PORT_OPENING_X_RANGE, port_y_range, USB_PORT_OPENING_Z_RANGE),
    ]
    cover = plate + front + tabs
    front_edges = cover.edges().filter_by(Axis.X).group_by(Axis.Y)[0]
    top_bend_edges = front_edges.group_by(Axis.Z)[-1]
    tab_bend_edges = [
        edge
        for x_range in TOP_COVER_TAB_X_RANGES
        for edge in front_edges.filter_by_position(Axis.X, *x_range).group_by(Axis.Z)[0]
    ]
    cover = fillet([*top_bend_edges, *tab_bend_edges], TOP_COVER_BEND_OUTER_RADIUS)
    cover = cover - plate_holes - tab_holes - frame_holes - port_openings
    cover = ENCLOSURE_LOCATION * cover
    cover.label = "enclosure_top_cover"
    return cover
