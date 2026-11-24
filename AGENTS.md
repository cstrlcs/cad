# cad

build123d models for 3D printing, as a uv workspace: one member package per topic under `packages/`, sharing the root `uv.lock`, `.venv` and `.python-version`.

- Read the `AGENTS.md` inside a package before changing it; its conventions apply only there.
- Create a new topic with `uv init --package packages/<name>` from the root, and add a dependency on another member with `uv add --package <name> <member>`.
- Run commands from the root: `uv run <script>`, where each package declares its script in `[project.scripts]`.
- Format and lint from the root with `uvx ruff format` and `uvx ruff check`; the strict rule set lives in the root `pyproject.toml`, and a finding is fixed at its cause, never silenced with `noqa` or a config change.
- Exported STL and DXF files are build outputs and stay out of git.
