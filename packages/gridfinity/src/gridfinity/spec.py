from build123d import Align, Part, Pos, RectangleRounded, extrude

GRID_PITCH = 42.0
HEIGHT_UNIT = 7.0

BASEPLATE_HEIGHT = 5.0
BASEPLATE_TOP_RADIUS = 4.0
BASEPLATE_PROFILE = ((0.7, 0.7), (0.0, 1.8), (2.15, 2.15))

BIN_GAP = 0.5
BIN_UNIT_SIZE = GRID_PITCH - BIN_GAP
BIN_OUTER_RADIUS = 3.75
BIN_BASE_PROFILE = ((0.8, 0.8), (0.0, 1.8), (2.15, 2.15))
BIN_FLOOR_TOP_Z = HEIGHT_UNIT

STACKING_LIP_PROFILE = ((0.7, 0.7), (0.0, 1.8), (1.9, 1.9))

MIN_CORNER = (Align.MIN, Align.MIN)


def profile_height(profile: tuple[tuple[float, float], ...]) -> float:
    return sum(rise for _, rise in profile)


def profile_inset(profile: tuple[tuple[float, float], ...]) -> float:
    return sum(run for run, _ in profile)


def profiled_block(
    top_width: float, top_length: float, top_radius: float, profile: tuple[tuple[float, float], ...]
) -> Part:
    inset = profile_inset(profile)
    block = Part()
    z = 0.0
    for run, rise in profile:
        outline = RectangleRounded(top_width - 2 * inset, top_length - 2 * inset, top_radius - inset)
        block += Pos(0, 0, z) * extrude(outline, rise, taper=-45 if run else 0)
        inset -= run
        z += rise
    return block


BASE_HEIGHT = profile_height(BIN_BASE_PROFILE)
STACKING_LIP_HEIGHT = profile_height(STACKING_LIP_PROFILE)
STACKING_LIP_DEPTH = profile_inset(STACKING_LIP_PROFILE)
