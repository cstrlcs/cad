from pathlib import Path

from build123d import ExportDXF, Unit, export_stl
from ocp_vscode import show

from ender3.assembly import upgraded_ender3_pro
from ender3.enclosure.accessories.camera_mount import camera_mount_for_printing
from ender3.enclosure.accessories.door_handle import door_handle_for_printing
from ender3.enclosure.accessories.door_magnet_catch import door_magnet_catch_for_printing
from ender3.enclosure.accessories.door_magnet_holder import door_magnet_holder_for_printing
from ender3.enclosure.accessories.hinge_door_leaf import hinge_door_leaf_for_printing
from ender3.enclosure.accessories.hinge_frame_leaf import hinge_frame_leaf_for_printing
from ender3.enclosure.accessories.power_switch_housing import power_switch_housing_for_printing
from ender3.enclosure.accessories.tripod_camera_case import tripod_camera_case
from ender3.enclosure.brackets.corner_bracket import corner_bracket_for_printing
from ender3.enclosure.brackets.rail_bracket import rail_bracket_for_printing
from ender3.enclosure.panels.laser_cut import laser_cut_outline, laser_cut_parts
from ender3.upgrades.bed_cable_strain_relief.bed_cable_strain_relief import bed_cable_strain_relief_for_printing
from ender3.upgrades.belt_tensioners.belt_tensioner_knob import belt_tensioner_knob
from ender3.upgrades.belt_tensioners.belt_tensioner_puller import belt_tensioner_puller_for_printing
from ender3.upgrades.belt_tensioners.idler_bushing import idler_bushing
from ender3.upgrades.belt_tensioners.x_belt_tensioner_body import x_belt_tensioner_body_for_printing
from ender3.upgrades.belt_tensioners.y_belt_tensioner_body import y_belt_tensioner_body_for_printing
from ender3.upgrades.board_cases.left_drawer import left_drawer_for_printing
from ender3.upgrades.board_cases.left_floor_tray import left_floor_tray_for_printing
from ender3.upgrades.board_cases.right_drawer import right_drawer_for_printing
from ender3.upgrades.board_cases.right_floor_tray import right_floor_tray_for_printing
from ender3.upgrades.fan_duct.hotend_shroud import hotend_shroud_for_printing
from ender3.upgrades.power_supply_case.left_power_supply_drawer import left_power_supply_drawer_for_printing
from ender3.upgrades.power_supply_case.right_power_supply_drawer import right_power_supply_drawer_for_printing
from ender3.upgrades.storage_drawers.left_storage_drawer import left_storage_drawer_for_printing
from ender3.upgrades.storage_drawers.left_storage_housing import left_storage_housing_for_printing
from ender3.upgrades.storage_drawers.right_storage_drawer import right_storage_drawer_for_printing
from ender3.upgrades.storage_drawers.right_storage_housing import right_storage_housing_for_printing
from ender3.upgrades.x_cable_chain.x_cable_chain_carriage_mount import x_cable_chain_carriage_mount_for_printing
from ender3.upgrades.x_cable_chain.x_cable_chain_fixed_mount import x_cable_chain_fixed_mount_for_printing
from ender3.upgrades.x_cable_chain.x_cable_chain_link import x_cable_chain_link
from ender3.upgrades.x_cable_chain.x_cable_chain_link_cover import x_cable_chain_link_cover_for_printing

STL_DIR = Path("stl")
DXF_DIR = Path("dxf")


def main() -> None:
    STL_DIR.mkdir(exist_ok=True)
    printable_parts = {
        "hotend_shroud": hotend_shroud_for_printing(),
        "bed_cable_strain_relief": bed_cable_strain_relief_for_printing(),
        "left_drawer": left_drawer_for_printing(),
        "right_drawer": right_drawer_for_printing(),
        "left_floor_tray": left_floor_tray_for_printing(),
        "right_floor_tray": right_floor_tray_for_printing(),
        "x_belt_tensioner_body": x_belt_tensioner_body_for_printing(),
        "y_belt_tensioner_body": y_belt_tensioner_body_for_printing(),
        "belt_tensioner_puller": belt_tensioner_puller_for_printing(),
        "belt_tensioner_knob": belt_tensioner_knob(),
        "idler_bushing": idler_bushing(),
        "left_storage_housing": left_storage_housing_for_printing(),
        "right_storage_housing": right_storage_housing_for_printing(),
        "left_storage_drawer": left_storage_drawer_for_printing(),
        "right_storage_drawer": right_storage_drawer_for_printing(),
        "left_power_supply_drawer": left_power_supply_drawer_for_printing(),
        "right_power_supply_drawer": right_power_supply_drawer_for_printing(),
        "corner_bracket": corner_bracket_for_printing(),
        "rail_bracket": rail_bracket_for_printing(),
        "hinge_frame_leaf": hinge_frame_leaf_for_printing(),
        "hinge_door_leaf": hinge_door_leaf_for_printing(),
        "door_magnet_holder": door_magnet_holder_for_printing(),
        "door_magnet_catch": door_magnet_catch_for_printing(),
        "door_handle": door_handle_for_printing(),
        "power_switch_housing": power_switch_housing_for_printing(),
        "camera_mount": camera_mount_for_printing(),
        "tripod_camera_case": tripod_camera_case(),
        "x_cable_chain_link": x_cable_chain_link(),
        "x_cable_chain_link_cover": x_cable_chain_link_cover_for_printing(),
        "x_cable_chain_fixed_mount": x_cable_chain_fixed_mount_for_printing(),
        "x_cable_chain_carriage_mount": x_cable_chain_carriage_mount_for_printing(),
    }
    for name, part in printable_parts.items():
        export_stl(part, STL_DIR / f"{name}.stl")
    DXF_DIR.mkdir(exist_ok=True)
    for name, part in laser_cut_parts().items():
        ExportDXF(unit=Unit.MM).add_shape(laser_cut_outline(part)).write(DXF_DIR / f"{name}.dxf")
    show(upgraded_ender3_pro())
