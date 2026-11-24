# gridfinity

Parametric Gridfinity baseplates and bins in build123d, for desk organisation printed on the Ender 3 Pro (bed 220 × 220 mm, so a baseplate is at most 5 × 5 units).

- Keep interface geometry (grid pitch, base, baseplate and stacking lip profiles) in `spec.py`, taken from https://gridfinity.xyz/specification/ and `src/core/standard.scad` / `src/core/gridfinity-baseplate.scad` in kennetek/gridfinity-rebuilt-openscad; a part that changes them stops fitting other Gridfinity parts.
- Build each part as a function of its unit counts, in millimetres, with the minimum corner at the origin and the bottom face on Z = 0, which is also its print orientation.
- Keep a bin's dividers below the stacking seat (`DIVIDER_TOP_BELOW_RIM`), so a bin stacked on top rests on the lip and not on the dividers.
