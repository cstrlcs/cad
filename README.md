# cad

Parametric 3D-printing models written in Python with [build123d](https://github.com/gumyr/build123d).

| Package | Contents |
| --- | --- |
| [`ender3`](packages/ender3) | Upgrades and an acrylic enclosure for a Creality Ender 3 Pro, built around a dimensional model of the stock printer |
| [`gridfinity`](packages/gridfinity) | [Gridfinity](https://gridfinity.xyz) baseplates, divider bins and a hardware box |

## Requirements

- [uv](https://docs.astral.sh/uv/), which installs Python 3.14 and the dependencies
- [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) for VS Code, to see the models

## Usage

```sh
uv sync
uv run ender3-cad
uv run gridfinity
```

Each command writes its STL files to `stl/` (and the laser-cut panels to `dxf/`) in the current directory, then opens the model in the viewer.

## Development

```sh
uvx ruff format
uvx ruff check
```

## License

[MIT](LICENSE). Models based on other people's work are credited in each package's README.
