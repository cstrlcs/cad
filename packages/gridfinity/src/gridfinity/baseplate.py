from build123d import Part, Pos, RectangleRounded, extrude

from gridfinity.spec import (
    BASEPLATE_HEIGHT,
    BASEPLATE_PROFILE,
    BASEPLATE_TOP_RADIUS,
    GRID_PITCH,
    MIN_CORNER,
    profile_height,
    profile_inset,
    profiled_block,
)

BIN_SEAT_CLEARANCE = BASEPLATE_HEIGHT - profile_height(BASEPLATE_PROFILE)


def baseplate(units_x: int, units_y: int) -> Part:
    plate = extrude(
        RectangleRounded(units_x * GRID_PITCH, units_y * GRID_PITCH, BASEPLATE_TOP_RADIUS, align=MIN_CORNER),
        BASEPLATE_HEIGHT,
    )
    inset = profile_inset(BASEPLATE_PROFILE)
    pocket = extrude(
        RectangleRounded(GRID_PITCH - 2 * inset, GRID_PITCH - 2 * inset, BASEPLATE_TOP_RADIUS - inset),
        BIN_SEAT_CLEARANCE,
    )
    pocket += Pos(0, 0, BIN_SEAT_CLEARANCE) * profiled_block(
        GRID_PITCH, GRID_PITCH, BASEPLATE_TOP_RADIUS, BASEPLATE_PROFILE
    )
    pocket += Pos(0, 0, BASEPLATE_HEIGHT) * extrude(
        RectangleRounded(GRID_PITCH, GRID_PITCH, BASEPLATE_TOP_RADIUS), BASEPLATE_HEIGHT
    )
    pockets = [
        Pos((i + 0.5) * GRID_PITCH, (j + 0.5) * GRID_PITCH, 0) * pocket for i in range(units_x) for j in range(units_y)
    ]
    plate -= pockets
    plate.label = f"baseplate_{units_x}x{units_y}"
    return plate
