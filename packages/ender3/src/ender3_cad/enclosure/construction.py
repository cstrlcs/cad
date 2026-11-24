from functools import cache
from typing import NamedTuple

from build123d import TOLERANCE, Axis, Compound, Cylinder, Location, Part, Plane, Pos, Vector, extrude

from ender3_cad.construction import block
from ender3_cad.dimensions import BOTTOM, M2_PILOT_DIAMETER
from ender3_cad.enclosure.dimensions import (
    CAMERA_CLEARANCE,
    CASE_INNER_HALF_WIDTH,
    CASE_INNER_TOP_Z,
    CASE_OUTER_HALF_WIDTH,
    CLEAR_PANEL_BOTTOM_Z,
    CUTTER_REACH,
    DOOR_BACK_Y,
    DOOR_FRONT_Y,
    DOOR_HARDWARE_CENTER_Z,
    HANDLE_CENTER_X,
    HANDLE_POST_CENTERS_Z,
    HINGE_AXIS,
    HINGE_SCREW_OFFSETS,
    LATCH_CATCH_DEPTH,
    LATCH_CATCH_FRONT_Y,
    LATCH_CENTER_X,
    LATCH_FEATURE_OFFSET,
    REAR_PANEL_FRONT_Y,
    SWITCH_CENTER_Y,
    SWITCH_CENTER_Z,
)
from ender3_cad.ender3.purchased.raspberry_pi_camera_module import (
    RASPBERRY_PI_CAMERA_BLOCK_SIZE,
    RASPBERRY_PI_CAMERA_CONNECTOR_SIZE,
    RASPBERRY_PI_CAMERA_LENS_CENTER,
    RASPBERRY_PI_CAMERA_LENS_TIP_HEIGHT,
    RASPBERRY_PI_CAMERA_MOUNTING_HOLES,
    RASPBERRY_PI_CAMERA_PCB_SIZE,
    RASPBERRY_PI_CAMERA_PCB_THICKNESS,
)
from ender3_cad.ender3.reference.electronics.dimensions import (
    POWER_SWITCH_BODY_Y,
    POWER_SWITCH_BODY_Z,
    POWER_SWITCH_SCREW_HOLES,
    POWER_SWITCH_SOLDER_TAB_X,
)
from ender3_cad.ender3.reference.y_axis.build_surface import build_surface
from ender3_cad.upgrades.board_cases.dimensions import RAIL_OUTER_FACE_X
from ender3_cad.upgrades.fan_duct.dimensions import MEASURED_NOZZLE_TIP

SIDE_BRACKET_Y = (-250.0, -60.0, 100.0)
RAIL_BRACKET_Y = (-100.0, 60.0)
TOP_REAR_BRACKET_X = (-150.0, 0.0, 150.0)
REAR_SIDE_BRACKET_EDGE_MARGIN = 12.0

SWITCH_CLEARANCE = 0.3
SWITCH_WIRING_SPACE = 10.0

CAMERA_LENS_YZ = (-240.0, 250.0)
CAMERA_TARGET_ABOVE_BED = 25.0
CAMERA_TARGET = Vector(0.0, MEASURED_NOZZLE_TIP.Y, build_surface().bounding_box().max.Z + CAMERA_TARGET_ABOVE_BED)
CAMERA_BACK_TO_PANEL = 12.0
CAMERA_FRAME_MARGIN = 5.0
CAMERA_FRAME_BLOCK_CLEARANCE = 0.4
CAMERA_FRAME_THICKNESS = RASPBERRY_PI_CAMERA_BLOCK_SIZE[2] + CAMERA_FRAME_BLOCK_CLEARANCE
CAMERA_WINDOW_X = (4.6, 20.4)

CAMERA_WALL_LENGTH = 80.0

CAMERA_FLANGE_MARGIN = 6.0
CAMERA_INSERT_INSET = 5.0


class BracketJoint(NamedTuple):
    corner: Vector
    u: Vector
    v: Vector
    leg_a_panel: str
    leg_b_panel: str


def hole(point: Vector, axis: Vector, diameter: float, length: float = 40.0) -> Part:
    return Plane(origin=point, z_dir=axis).location * Cylinder(diameter / 2, length)


def blind_hole(point: Vector, axis: Vector, diameter: float, depth: float) -> Part:
    return Plane(origin=point, z_dir=axis).location * Cylinder(diameter / 2, depth, align=BOTTOM)


def side_panel_name(side: int) -> str:
    return "left_side_panel" if side < 0 else "right_side_panel"


def bottom_panel_name(side: int) -> str:
    return "left_bottom_panel" if side < 0 else "right_bottom_panel"


@cache
def bracket_joints() -> tuple[BracketJoint, ...]:
    inner, top, rear = CASE_INNER_HALF_WIDTH, CASE_INNER_TOP_Z, REAR_PANEL_FRONT_Y
    up, down, toward_front = Vector(0, 0, 1), Vector(0, 0, -1), Vector(0, -1, 0)
    rear_side_z = (
        CLEAR_PANEL_BOTTOM_Z + REAR_SIDE_BRACKET_EDGE_MARGIN,
        (CLEAR_PANEL_BOTTOM_Z + top) / 2,
        top - REAR_SIDE_BRACKET_EDGE_MARGIN,
    )
    joints = [
        BracketJoint(Vector(x, rear, top), toward_front, down, "top_panel", "rear_panel") for x in TOP_REAR_BRACKET_X
    ]
    for side in (-1, 1):
        inward = Vector(-side, 0, 0)
        side_panel, bottom_panel = side_panel_name(side), bottom_panel_name(side)
        joints += [
            BracketJoint(Vector(side * inner, rear, z), inward, toward_front, "rear_panel", side_panel)
            for z in rear_side_z
        ]
        joints += [
            BracketJoint(Vector(side * inner, y, top), inward, down, "top_panel", side_panel) for y in SIDE_BRACKET_Y
        ]
        joints += [
            BracketJoint(Vector(side * RAIL_OUTER_FACE_X, y, 0), Vector(side, 0, 0), up, bottom_panel, "rail")
            for y in RAIL_BRACKET_Y
        ]
    return tuple(joints)


def door_hinge_screw_points(center_z: float) -> list[Vector]:
    return [Vector(HINGE_AXIS.X + offset, DOOR_FRONT_Y, center_z) for offset in HINGE_SCREW_OFFSETS]


def frame_hinge_screw_points(center_z: float) -> list[Vector]:
    return [Vector(-CASE_OUTER_HALF_WIDTH, HINGE_AXIS.Y + offset, center_z) for offset in HINGE_SCREW_OFFSETS]


def latch_holder_screw_point() -> Vector:
    return Vector(LATCH_CENTER_X, DOOR_BACK_Y, DOOR_HARDWARE_CENTER_Z - LATCH_FEATURE_OFFSET)


def latch_catch_screw_point() -> Vector:
    return Vector(
        CASE_INNER_HALF_WIDTH,
        LATCH_CATCH_FRONT_Y + LATCH_CATCH_DEPTH / 2,
        DOOR_HARDWARE_CENTER_Z - LATCH_FEATURE_OFFSET,
    )


def handle_screw_points() -> list[Vector]:
    return [Vector(HANDLE_CENTER_X, DOOR_FRONT_Y, z) for z in HANDLE_POST_CENTERS_Z]


def switch_cavity_ranges() -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    cavity_x = (-CASE_INNER_HALF_WIDTH, -CASE_OUTER_HALF_WIDTH - POWER_SWITCH_SOLDER_TAB_X[0] + SWITCH_WIRING_SPACE)
    cavity_y = (
        SWITCH_CENTER_Y - POWER_SWITCH_BODY_Y[1] - SWITCH_CLEARANCE,
        SWITCH_CENTER_Y - POWER_SWITCH_BODY_Y[0] + SWITCH_CLEARANCE,
    )
    cavity_z = (
        SWITCH_CENTER_Z + POWER_SWITCH_BODY_Z[0] - SWITCH_CLEARANCE,
        SWITCH_CENTER_Z + POWER_SWITCH_BODY_Z[1] + SWITCH_CLEARANCE,
    )
    return cavity_x, cavity_y, cavity_z


def switch_screw_points() -> list[Vector]:
    return [
        Vector(-CASE_OUTER_HALF_WIDTH, SWITCH_CENTER_Y - y, SWITCH_CENTER_Z + z) for y, z in POWER_SWITCH_SCREW_HOLES
    ]


def _camera_plane(tip: Vector) -> Location:
    forward = (CAMERA_TARGET - tip).normalized()
    up = (Vector(0, 0, 1) - forward * forward.Z).normalized()
    right = up.cross(forward)
    lens_x, lens_y = RASPBERRY_PI_CAMERA_LENS_CENTER
    origin = tip - right * lens_x - up * lens_y - forward * RASPBERRY_PI_CAMERA_LENS_TIP_HEIGHT
    return Plane(origin=tuple(origin), x_dir=tuple(right), z_dir=tuple(forward)).location


def _camera_back_envelope() -> Part:
    width, height = RASPBERRY_PI_CAMERA_PCB_SIZE
    c = CAMERA_CLEARANCE
    depth = RASPBERRY_PI_CAMERA_PCB_THICKNESS + RASPBERRY_PI_CAMERA_CONNECTOR_SIZE[2] + c
    return block((-c, width + c), (-c, height + c), (-depth, 0))


@cache
def camera_location() -> Location:
    back_x_target = CASE_INNER_HALF_WIDTH - CAMERA_BACK_TO_PANEL
    envelope = _camera_back_envelope()
    tip = Vector(back_x_target, *CAMERA_LENS_YZ)
    while True:
        correction = back_x_target - (_camera_plane(tip) * envelope).bounding_box().max.X
        if abs(correction) < TOLERANCE:
            return _camera_plane(tip)
        tip += Vector(correction, 0, 0)


@cache
def camera_insert_points() -> tuple[Vector, Vector]:
    (y0, y1), (z0, z1) = camera_flange_ranges()
    inset = CAMERA_INSERT_INSET
    return (
        Vector(CASE_INNER_HALF_WIDTH, y0 + inset, z0 + inset),
        Vector(CASE_INNER_HALF_WIDTH, y1 - inset, z1 - inset),
    )


def _swept_to_right_panel(part: Part) -> Part:
    faces = part.faces().filter_by(lambda face: face.normal_at().X > TOLERANCE)
    swept = part + [extrude(face, 2 * CAMERA_WALL_LENGTH, dir=(1, 0, 0)) for face in faces]
    return swept & block(
        (-CUTTER_REACH, CASE_INNER_HALF_WIDTH), (-CUTTER_REACH, CUTTER_REACH), (-CUTTER_REACH, CUTTER_REACH)
    )


def camera_holder() -> Part:
    width, height = RASPBERRY_PI_CAMERA_PCB_SIZE
    m, t = CAMERA_FRAME_MARGIN, CAMERA_FRAME_THICKNESS
    rows = (-m, height + m)
    strips = block((-m, CAMERA_WINDOW_X[0]), rows, (0, t)) + block((CAMERA_WINDOW_X[1], width + m), rows, (0, t))
    pilots = [
        Pos(x, y, 0) * Cylinder(M2_PILOT_DIAMETER / 2, t, align=BOTTOM) for x, y in RASPBERRY_PI_CAMERA_MOUNTING_HOLES
    ]
    window = block(CAMERA_WINDOW_X, (-CUTTER_REACH, CUTTER_REACH), (0, CUTTER_REACH))
    location = camera_location()
    return _swept_to_right_panel(location * strips) - location * (window + pilots)


@cache
def camera_flange_ranges() -> tuple[tuple[float, float], tuple[float, float]]:
    footprint = Compound(camera_holder().faces().group_by(Axis.X)[-1]).bounding_box()
    margin = CAMERA_FLANGE_MARGIN
    return (footprint.min.Y - margin, footprint.max.Y + margin), (footprint.min.Z - margin, footprint.max.Z + margin)
