from build123d import Compound, Pos

from ender3.enclosure.accessories.camera_mount import camera_mount
from ender3.enclosure.accessories.door_handle import door_handle
from ender3.enclosure.accessories.door_magnet_catch import door_magnet_catch
from ender3.enclosure.accessories.door_magnet_holder import door_magnet_holder
from ender3.enclosure.accessories.hinge_door_leaf import hinge_door_leaf
from ender3.enclosure.accessories.hinge_frame_leaf import hinge_frame_leaf
from ender3.enclosure.accessories.power_switch_housing import power_switch_housing
from ender3.enclosure.brackets.case_brackets import case_brackets
from ender3.enclosure.dimensions import BED_SHIFT_AT_Y_HOME, HINGE_CENTERS_Z
from ender3.enclosure.panels.front_center_plate import front_center_plate
from ender3.enclosure.panels.front_door import front_door
from ender3.enclosure.panels.left_bottom_panel import left_bottom_panel
from ender3.enclosure.panels.left_side_panel import left_side_panel
from ender3.enclosure.panels.rear_center_plate import rear_center_plate
from ender3.enclosure.panels.rear_panel import rear_panel
from ender3.enclosure.panels.right_bottom_panel import right_bottom_panel
from ender3.enclosure.panels.right_side_panel import right_side_panel
from ender3.enclosure.panels.top_panel import top_panel
from ender3.ender3.bed_heater_cable import bed_heater_cable
from ender3.ender3.bed_probe import bed_probe
from ender3.ender3.buck_converter import buck_converter
from ender3.ender3.hotend_fan_4010 import hotend_fan_4010
from ender3.ender3.left_drawer_fan import left_drawer_fan
from ender3.ender3.mainboard_4_2_7 import mainboard_4_2_7
from ender3.ender3.mains_power_switch import mains_power_switch
from ender3.ender3.mean_well_power_supply import mean_well_power_supply
from ender3.ender3.part_cooling_blower import part_cooling_blower
from ender3.ender3.raspberry_pi import raspberry_pi
from ender3.ender3.raspberry_pi_camera import raspberry_pi_camera
from ender3.ender3.reference import ender3_pro
from ender3.ender3.right_drawer_fan import right_drawer_fan
from ender3.upgrades.bed_cable_strain_relief.bed_cable_strain_relief import bed_cable_strain_relief
from ender3.upgrades.belt_tensioners.assembly import x_belt_tensioner_assembly, y_belt_tensioner_assembly
from ender3.upgrades.board_cases.left_drawer import left_drawer
from ender3.upgrades.board_cases.left_floor_tray import left_floor_tray
from ender3.upgrades.board_cases.right_drawer import right_drawer
from ender3.upgrades.board_cases.right_floor_tray import right_floor_tray
from ender3.upgrades.fan_duct.hotend_shroud import hotend_shroud
from ender3.upgrades.power_supply_case.left_power_supply_drawer import left_power_supply_drawer
from ender3.upgrades.power_supply_case.right_power_supply_drawer import right_power_supply_drawer
from ender3.upgrades.storage_drawers.left_storage_drawer import left_storage_drawer
from ender3.upgrades.storage_drawers.left_storage_housing import left_storage_housing
from ender3.upgrades.storage_drawers.right_storage_drawer import right_storage_drawer
from ender3.upgrades.storage_drawers.right_storage_housing import right_storage_housing
from ender3.upgrades.x_cable_chain.assembly import x_cable_chain_parts

REPLACED_STOCK_PARTS = {
    "fan_cover",
    "hotend_fan",
    "part_cooling_fan",
    "part_cooling_duct",
    "z_endstop_bracket",
    "z_endstop_switch",
    "x_belt_tensioner",
    "y_belt_tensioner",
    "y_belt_tensioner_idler_bushing",
    "power_supply",
    "power_supply_bracket",
    "power_switch",
    "enclosure_bottom_cover",
    "enclosure_top_cover",
    "case_fan",
    "mainboard",
}
BED_MOVING_PARTS = {
    "bed_carriage_plate",
    "heated_bed",
    "build_surface",
    "front_belt_end_sleeve",
    "rear_belt_end_sleeve",
    "front_left_wheel",
    "front_right_wheel",
    "rear_left_wheel",
    "rear_right_wheel",
    "front_left_wheel_spacer",
    "rear_left_wheel_spacer",
    "front_right_eccentric_spacer",
    "rear_right_eccentric_spacer",
}
AT_Y_HOME = Pos(0, BED_SHIFT_AT_Y_HOME, 0)


def ender3() -> Compound:
    subsystems = {subsystem.label: subsystem for subsystem in ender3_pro().children}
    for subsystem in subsystems.values():
        subsystem.children = [part for part in subsystem.children if part.label not in REPLACED_STOCK_PARTS]
    y_axis = subsystems["y_axis"]
    y_axis.children = [
        *[AT_Y_HOME * part if part.label in BED_MOVING_PARTS else part for part in y_axis.children],
        AT_Y_HOME * bed_heater_cable(),
    ]
    print_head = subsystems["print_head"]
    print_head.children = [*print_head.children, hotend_fan_4010(), part_cooling_blower(), bed_probe()]
    electronics = subsystems["electronics"]
    electronics.children = [
        *electronics.children,
        mainboard_4_2_7(),
        left_drawer_fan(),
        raspberry_pi(),
        right_drawer_fan(),
        buck_converter(),
        mean_well_power_supply(),
        mains_power_switch(),
        raspberry_pi_camera(),
    ]
    return Compound(label="ender3", children=list(subsystems.values()))


def upgrades() -> Compound:
    return Compound(
        label="upgrades",
        children=[
            Compound(label="fan_duct", children=[hotend_shroud()]),
            Compound(
                label="board_cases",
                children=[left_drawer(), left_floor_tray(), right_drawer(), right_floor_tray()],
            ),
            Compound(
                label="power_supply_case",
                children=[left_power_supply_drawer(), right_power_supply_drawer()],
            ),
            Compound(
                label="storage_drawers",
                children=[
                    left_storage_housing(),
                    right_storage_housing(),
                    left_storage_drawer(),
                    right_storage_drawer(),
                ],
            ),
            Compound(label="belt_tensioners", children=[x_belt_tensioner_assembly(), y_belt_tensioner_assembly()]),
            Compound(label="bed_cable_strain_relief", children=[AT_Y_HOME * bed_cable_strain_relief()]),
            Compound(label="x_cable_chain", children=x_cable_chain_parts()),
        ],
    )


def enclosure() -> Compound:
    return Compound(
        label="enclosure",
        children=[
            Compound(
                label="panels",
                children=[
                    front_door(),
                    rear_panel(),
                    left_side_panel(),
                    right_side_panel(),
                    top_panel(),
                    left_bottom_panel(),
                    right_bottom_panel(),
                    front_center_plate(),
                    rear_center_plate(),
                ],
            ),
            Compound(label="brackets", children=case_brackets()),
            Compound(
                label="accessories",
                children=[
                    *(hinge_frame_leaf(index) for index in range(len(HINGE_CENTERS_Z))),
                    *(hinge_door_leaf(index) for index in range(len(HINGE_CENTERS_Z))),
                    door_magnet_holder(),
                    door_magnet_catch(),
                    door_handle(),
                    power_switch_housing(),
                    camera_mount(),
                ],
            ),
        ],
    )


def upgraded_ender3_pro() -> Compound:
    return Compound(label="upgraded_ender3_pro", children=[ender3(), upgrades(), enclosure()])
