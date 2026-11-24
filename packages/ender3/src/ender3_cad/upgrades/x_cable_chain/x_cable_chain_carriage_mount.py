from build123d import Cylinder, Part, Plane, Polygon, Pos, Rot, Vector, extrude

from ender3_cad.colors import PRINTED_PART_COLOR
from ender3_cad.construction import block, resting_on_bed
from ender3_cad.dimensions import BOTTOM, CUT_OVERSHOOT, FACE_DOWN, M3_CLEARANCE_DIAMETER
from ender3_cad.ender3.reference.components.dimensions import FAN_4010_MOUNTING_HOLES, FAN_4010_SIZE
from ender3_cad.ender3.reference.print_head.dimensions import HOTEND_AXIS_X
from ender3_cad.upgrades.fan_duct.dimensions import HOTEND_FAN_LOCATION
from ender3_cad.upgrades.x_cable_chain.construction import chain_frame, male_end, mirrored_x_ranges
from ender3_cad.upgrades.x_cable_chain.dimensions import (
    CABLE_WINDOW_LENGTH,
    CARRIAGE_PIVOT_X,
    CHAIN_AXIS_Z,
    CHAIN_Z_RANGE,
    INNER_PLATE_X,
    LINK_HEIGHT,
    LINK_WIDTH,
    MOUNT_BODY_LENGTH,
    MOVING_RUN_Y,
    OUTER_ZONE_START_Y,
)

FAN_TOP_FRONT_EDGE = (HOTEND_FAN_LOCATION * Pos(0, -FAN_4010_SIZE / 2, 0)).position
UPPER_FAN_HOLES = [(x, y) for x, y in FAN_4010_MOUNTING_HOLES if y < 0]
MOUNT_PLATE_REINFORCEMENT = 2.0
FAN_SCREW_HEAD_DIAMETER = 6.5
FAN_SCREW_HEAD_SEAT = 3.0
FAN_EDGE_CLEARANCE = 0.2
CARRIAGE_WEB_HALF_WIDTH = 21.5
CARRIAGE_WEB_BACK_Y = FAN_TOP_FRONT_EDGE.Y - FAN_EDGE_CLEARANCE
CARRIAGE_WEB_BOTTOM_Z = 288.0
CARRIAGE_WEB_DROP_BELOW_CHAIN = 5.0
CARRIAGE_WEB_TOP_Z = CHAIN_Z_RANGE[0] - CARRIAGE_WEB_DROP_BELOW_CHAIN
CARRIAGE_POST_BOTTOM_Z = 300.0
BODY_WEB_OVERLAP = 4.0
FAN_INTAKE_KEEP_OUT_HALF_WIDTH = 11.5
FAN_INTAKE_KEEP_OUT_TOP_Z = FAN_TOP_FRONT_EDGE.Z + 2 * FAN_EDGE_CLEARANCE


def _web(body_x: tuple[float, float]) -> Part:
    body_back_y = MOVING_RUN_Y - LINK_HEIGHT / 2
    body_front_y = MOVING_RUN_Y + LINK_HEIGHT / 2
    web_x = (HOTEND_AXIS_X - CARRIAGE_WEB_HALF_WIDTH, HOTEND_AXIS_X + CARRIAGE_WEB_HALF_WIDTH)
    joint_top_z = CHAIN_Z_RANGE[0] + BODY_WEB_OVERLAP
    outline = Polygon(
        (body_x[0], body_front_y),
        (body_x[1], body_front_y),
        (web_x[1], CARRIAGE_WEB_BACK_Y),
        (web_x[0], CARRIAGE_WEB_BACK_Y),
        align=None,
    )
    plan = Pos(0, 0, CARRIAGE_WEB_BOTTOM_Z) * extrude(outline, joint_top_z - CARRIAGE_WEB_BOTTOM_Z)
    side_profile = Polygon(
        (body_front_y, CARRIAGE_POST_BOTTOM_Z),
        (body_front_y, joint_top_z),
        (body_front_y + joint_top_z - CARRIAGE_WEB_TOP_Z, CARRIAGE_WEB_TOP_Z),
        (CARRIAGE_WEB_BACK_Y, CARRIAGE_WEB_TOP_Z),
        (CARRIAGE_WEB_BACK_Y, CARRIAGE_WEB_BOTTOM_Z),
        (body_front_y + CARRIAGE_POST_BOTTOM_Z - CARRIAGE_WEB_BOTTOM_Z, CARRIAGE_WEB_BOTTOM_Z),
        align=None,
    )
    span_x = (min(body_x[0], web_x[0]) - CUT_OVERSHOOT, max(body_x[1], web_x[1]) + CUT_OVERSHOOT)
    side = Pos(span_x[0], 0, 0) * extrude(Plane.YZ * side_profile, span_x[1] - span_x[0], dir=(1, 0, 0))
    web = (plan & side) + block(body_x, (body_back_y, body_front_y), (CARRIAGE_POST_BOTTOM_Z, CHAIN_Z_RANGE[0]))
    intake = (HOTEND_AXIS_X - FAN_INTAKE_KEEP_OUT_HALF_WIDTH, HOTEND_AXIS_X + FAN_INTAKE_KEEP_OUT_HALF_WIDTH)
    web -= block(intake, (body_front_y, CARRIAGE_WEB_BACK_Y), (CARRIAGE_WEB_BOTTOM_Z, FAN_INTAKE_KEEP_OUT_TOP_Z))
    web -= HOTEND_FAN_LOCATION * block(
        (-FAN_4010_SIZE, FAN_4010_SIZE), (-FAN_4010_SIZE, FAN_4010_SIZE), (0, FAN_4010_SIZE)
    )
    web -= [
        HOTEND_FAN_LOCATION
        * Pos(x, y, 0)
        * FACE_DOWN
        * (
            Cylinder(M3_CLEARANCE_DIAMETER / 2, FAN_SCREW_HEAD_SEAT, align=BOTTOM)
            + Pos(0, 0, FAN_SCREW_HEAD_SEAT) * Cylinder(FAN_SCREW_HEAD_DIAMETER / 2, FAN_4010_SIZE, align=BOTTOM)
        )
        for x, y in UPPER_FAN_HOLES
    ]
    return web


def x_cable_chain_carriage_mount() -> Part:
    window_end = -OUTER_ZONE_START_Y + CABLE_WINDOW_LENGTH
    half_width = LINK_WIDTH / 2
    reinforcements = [
        block(x_range, (-OUTER_ZONE_START_Y, window_end), (0, LINK_HEIGHT))
        for x_range in mirrored_x_ranges(INNER_PLATE_X - MOUNT_PLATE_REINFORCEMENT, MOUNT_PLATE_REINFORCEMENT)
    ]
    chain_end = male_end(window_end) + reinforcements
    chain_end += block((-half_width, half_width), (window_end, window_end + MOUNT_BODY_LENGTH), (0, LINK_HEIGHT))
    pivot = Vector(CARRIAGE_PIVOT_X, MOVING_RUN_Y, CHAIN_AXIS_Z)
    mount = chain_frame(pivot, Vector(-1, 0, 0)) * chain_end
    mount += _web((pivot.X - window_end - MOUNT_BODY_LENGTH, pivot.X - window_end))
    mount.label = "x_cable_chain_carriage_mount"
    mount.color = PRINTED_PART_COLOR
    return mount


def x_cable_chain_carriage_mount_for_printing() -> Part:
    return resting_on_bed(Rot(90, 0, 0) * x_cable_chain_carriage_mount())
