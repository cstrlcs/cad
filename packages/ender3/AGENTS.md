# ender3

build123d models of upgrades and accessories for a stock Creality Ender 3 Pro, designed against the dimensional reference model in `src/ender3/ender3/reference/`.

## Commands

- `uv run ender3` rebuilds every STL and DXF and sends the tree to the OCP CAD Viewer.

## Architecture

The package layout mirrors the viewer tree, whose root groups are `ender3`, `upgrades` and `enclosure`.

| What | Where |
| --- | --- |
| Stock printer part | `src/ender3/ender3/reference/<subsystem>/<part>.py` |
| Bought component, in its own frame | `src/ender3/ender3/purchased/<part>.py` |
| Bought component placed in the printer (fans, boards, PSU, camera) | `src/ender3/ender3/<part>.py` |
| Printed upgrade | `src/ender3/upgrades/<group>/<part>.py` |
| Acrylic panel, corner bracket, case accessory | `src/ender3/enclosure/{panels,brackets,accessories}/<part>.py` |
| Viewer tree and the stock parts the upgrades replace | `src/ender3/assembly.py` |
| STL export list | `main()` in `src/ender3/__init__.py` |
| DXF export list | `laser_cut_parts()` in `src/ender3/enclosure/panels/laser_cut.py` |

- Keep one part per file, named after its part function; the file also holds the constants and helpers only that part uses, and a `<part>_for_printing()` when the print pose differs from the assembled pose.
- Put a constant used by several files in the `dimensions.py`, and a helper in the `construction.py`, of the nearest package that contains every user. A bought part's own specification constants stay in its `purchased/<part>.py` and are imported from there.
- Keep `__init__.py` files empty outside `ender3/reference/`, because `enclosure` and `upgrades` import each other's modules and a package-level import there creates a cycle.
- Label every part with the name of its part function, including bought parts placed in the printer.
- When a new part replaces a stock part, add the stock part's label to `REPLACED_STOCK_PARTS` in `src/ender3/assembly.py`.

## Conventions

- Treat `src/ender3/ender3/reference/` as a fixed reference of the stock printer: new parts live outside it and import its parts and constants.
- Leave stock Ender 3 parts without a color, so the OCP CAD Viewer shows them in its default yellow (`#E8B024`).
- Color every printed part with `PRINTED_PART_COLOR` (blue) and every bought part with `PURCHASED_PART_COLOR` (grey), both from `src/ender3/colors.py`, so they stand out against the stock parts.
