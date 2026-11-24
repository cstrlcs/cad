# Ender 3 Pro reference model

Dimensional reference of the stock Creality Ender 3 Pro, written in build123d, for designing upgrades and accessories. It is not meant to be printed.

## Source and credits

Recreated from the STEP file `01 MAIN ASM Ender 3 Pro.STEP` (SolidWorks 2018 export, 2019-10-07) published by [hyotynen](https://github.com/hyotynen) in [hyotynen/Ender-3-Pro — 3D Model](https://github.com/hyotynen/Ender-3-Pro/tree/master/3D%20Model). That model is in turn based on the Ender 3 model by GitHub user Sleeepy in Creality's official repository [Creality3DPrinting/Ender-3](https://github.com/Creality3DPrinting/Ender-3/tree/master/Ender-3%20Mechanical/Ender-3%20Parts) (GPL-3.0). The hyotynen repository declares no license.

## Coordinate frame

All units are millimetres. X+ points right seen from the front, Y+ toward the back, Z+ up. Z=0 is the underside of the base extrusions and X=0 is the frame centreline. The origin is the STEP's origin, rotated +90° about X.

The moving axes stay where the source model has them: bed (Y), gantry height (Z) and print head (X).

## Usage

```python
from ender3_cad.ender3.reference import ender3_pro
from ender3_cad.ender3.reference.print_head.nozzle import NOZZLE_TIP
from ender3_cad.ender3.reference.print_head.x_carriage_plate import x_carriage_plate
from ender3_cad.ender3.reference.profiles.vslot_2020 import vslot_2020
```

`uv run ender3-cad` shows the whole printer in the OCP CAD Viewer.

Every part is a public function that takes no arguments and returns the part already placed in the printer frame, labelled with its own name, in a file of its own named after the function. Each subsystem is a package whose `__init__.py` holds an assembly function named after it, and `ender3_pro()` combines them. Every meaningful dimension, hole position and placement is a module-level constant: in the part's file when only that part uses it, otherwise in the subsystem's `dimensions.py`, or in `reference/dimensions.py` when several subsystems share it. Helpers follow the same rule with `construction.py`.

| Package | Contents |
|---|---|
| `profiles` | V-slot 2020/2040/4040 sections with the exact slot geometry. These are local, unplaced extrusions. |
| `components` | Standard parts in their local frames: NEMA17 steppers, V-wheel, spacers, eccentric spacer, limit switch, GT2 pulleys, 4010 fan, F688 bearing, belt-end sleeve. |
| `frame` | Base rails, middle cross member, Y rail, uprights and top bar, with their machining. |
| `y_axis` | Carriage plate, heated bed, build surface, Y motor and holder, belt tensioner, endstop, wheels. |
| `z_axis` | Z motor, motor bracket, coupler, lead screw, endstop. |
| `x_axis` | X beam, gantry plates, X motor, belt tensioner, endstop, lead-screw nut, wheels. |
| `extruder` | Extruder motor bracket (also the rear left gantry plate), motor, housing, idler arm, drive gear, bowden coupler. |
| `print_head` | X carriage plate, hotend (heatsink, heater block, nozzle), fan cover, hotend fan, part-cooling blower and duct, wheels. |
| `electronics` | Enclosure covers, mainboard, case fan, PSU, PSU bracket, power switch. |

## Fidelity

Each part was compared against its STEP part with three checks:

- bounding box
- every cylindrical hole: diameter and axis
- a boolean symmetric difference, or point sampling where OpenCascade's booleans fail

Results:

- Bounding boxes match within 0.01 mm on 93 of 95 parts. The other two are the extruder housing and idler arm, whose 0.3 mm embossed logos were dropped. Every functional hole matches.
- Custom parts are within 0.8% of the STEP's volume, apart from two cases. The part-cooling duct is at 1.1% because four small fillets inside its channel were left out. The lead screw is the other exception, described below.
- Purchased parts are within 0.4%, except the axial fans (about 2%, no blades) and the extruder's bowden coupler (5.4%, thread at major diameter).

Deliberate simplifications:

- **Lead screw:** a plain Ø8 × 370 cylinder without the thread helix.
- **Axial fans:** blades left out. The part-cooling blower keeps its rotor blades.
- **Bowden couplers:** threads modelled at major diameter.
- **Small cosmetic rounds:** 0.2 mm profile edges, sheet-metal bend rounds and small fillets left out.
- **Embossed logos:** left out.

Not modelled: fasteners, T-nuts, belts, springs, bed-leveling knobs, extrusion end caps, rubber feet, LCD and its bracket, spool holder, heater cartridge, thermistor, and the 625 bearings inside the V-wheels.

Errors in the source STEP were reproduced as they are:

- **PSU bracket:** has no holes for two of the PSU screws.
- **Mainboard:** has no standoffs.
- **Y rail:** carries a stray duplicate body, which was dropped.
