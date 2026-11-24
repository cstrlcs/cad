# gridfinity

Parametric [Gridfinity](https://gridfinity.xyz) parts for desk organisation, sized for the Ender 3 Pro bed (220 × 220 mm, so up to 5 × 5 units).

```sh
uv run gridfinity
```

This command writes the STL files to `stl/` and shows the parts seated on the baseplate in the OCP CAD Viewer.

| Part | Function |
| --- | --- |
| Baseplate | `baseplate(units_x, units_y)` |
| Bin with optional compartments | `gridfinity_bin(units_x, units_y, height_units, compartments_x, compartments_y)` |
| Hardware box with a pen channel, one compartment per thread size (M2 to M5) and a lid labelled with those sizes | `hardware_box(units_x, units_y, height_units)`, `hardware_box_lid(units_x, units_y, height_units)` |

Every part is built in millimetres, with its minimum corner at the origin and its bottom face on Z = 0, which is also its print orientation.

## Credits

| Part | Based on | Author | License |
| --- | --- | --- | --- |
| Grid, base, baseplate and stacking lip profiles (`src/gridfinity/spec.py`) | [Gridfinity specification](https://gridfinity.xyz/specification/) and [gridfinity-rebuilt-openscad](https://github.com/kennetek/gridfinity-rebuilt-openscad) | Zack Freedman (Gridfinity), Kenneth Hodson (gridfinity-rebuilt-openscad) | [MIT](https://github.com/kennetek/gridfinity-rebuilt-openscad/blob/main/LICENSE) |
