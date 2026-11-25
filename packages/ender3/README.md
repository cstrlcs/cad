# ender3

Upgrades and an acrylic enclosure for a stock Creality Ender 3 Pro. Each part is designed against a [dimensional model of the stock printer](src/ender3/ender3/reference/README.md), so it fits the real machine without test prints.

```sh
uv run ender3
```

This command writes every printed part to `stl/` and every acrylic panel to `dxf/`, then shows the upgraded printer in the OCP CAD Viewer. Stock parts are yellow, printed parts blue and bought parts grey.

## Upgrades

| Group | Parts |
| --- | --- |
| `fan_duct` | Hotend shroud for a 4010 hotend fan and a 5015 part-cooling blower |
| `board_cases` | Drawers and floor trays under the printer for the Creality 4.2.7 board, a Raspberry Pi 3B, an LM2596 buck converter and their fans |
| `power_supply_case` | Two drawer halves holding a Mean Well power supply |
| `storage_drawers` | Storage housings and drawers |
| `belt_tensioners` | X and Y belt tensioners with a knob, puller and idler bushing |
| `bed_cable_strain_relief` | Strain relief for the heated bed cable |
| `x_cable_chain` | Cable chain links, covers and mounts for the X axis |

## Enclosure

| Group | Parts |
| --- | --- |
| `panels` | Door, side, rear and top panels in 4 mm clear acrylic, and bottom and centre plates in 3 mm black acrylic, exported as DXF for laser cutting |
| `brackets` | Printed corner and rail brackets that join the panels |
| `accessories` | Hinges, magnetic door latch, handle, power switch housing, camera mount and a tripod camera case |

## Credits

| Part | Based on | Author | License |
| --- | --- | --- | --- |
| Stock printer reference (`src/ender3/ender3/reference/`) | Redrawn from the [Ender 3 Pro STEP model](https://github.com/hyotynen/Ender-3-Pro/tree/master/3D%20Model), itself based on [Creality's Ender 3 model](https://github.com/Creality3DPrinting/Ender-3); see [its README](src/ender3/ender3/reference/README.md) | hyotynen; Creality | None declared; [GPL-3.0](https://github.com/Creality3DPrinting/Ender-3/blob/master/LICENSE) |
| Hotend shroud (`src/ender3/upgrades/fan_duct/`) | Remix of [Mini-Me v4 lightweight Ender3 Hotend Duct](https://www.printables.com/model/197957-mini-me-v4-lightweight-ender3-hotend-duct-stock-pa) | Philipp | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| X cable chain (`src/ender3/upgrades/x_cable_chain/`) | Link pitch, width, height, pin and plate sizes and the horizontal chain layout from [Slim X Axis Cable Chain with Extruder and Hotend Mount for Ender 3 Pro](https://www.thingiverse.com/thing:4314829); geometry redrawn, mounts redesigned to keep clear of an extruder-top filament sensor | norp | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
