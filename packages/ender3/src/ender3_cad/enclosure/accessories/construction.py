from math import sqrt

from build123d import Cylinder, Part, Pos, Vector

from ender3_cad.dimensions import BOTTOM
from ender3_cad.enclosure.dimensions import HINGE_AXIS, HINGE_KNUCKLE_RADIUS

HINGE_HEIGHT = 42.0
HINGE_KNUCKLE_GAP = 0.4
HINGE_PIN_DIAMETER = 3.4

HINGE_SWEEP_RADIUS = sqrt(2) * HINGE_KNUCKLE_RADIUS


def hinge_z_range(center_z: float) -> tuple[float, float]:
    return center_z - HINGE_HEIGHT / 2, center_z + HINGE_HEIGHT / 2


def hinge_knuckle_ranges(center_z: float) -> tuple[tuple[float, float], ...]:
    bottom = center_z - HINGE_HEIGHT / 2
    third = HINGE_HEIGHT / 3
    gap = HINGE_KNUCKLE_GAP / 2
    return (
        (bottom, bottom + third - gap),
        (bottom + third + gap, bottom + 2 * third - gap),
        (
            bottom + 2 * third + gap,
            bottom + HINGE_HEIGHT,
        ),
    )


def _knuckle(axis: Vector, radius: float, z_range: tuple[float, float]) -> Part:
    return Pos(axis.X, axis.Y, z_range[0]) * Cylinder(radius, z_range[1] - z_range[0], align=BOTTOM)


def knuckled_leaf(
    plate: Part, center_z: float, own: tuple[tuple[float, float], ...], other: tuple[tuple[float, float], ...]
) -> Part:
    half_gap = HINGE_KNUCKLE_GAP / 2
    leaf = plate - [
        _knuckle(HINGE_AXIS, HINGE_SWEEP_RADIUS + HINGE_KNUCKLE_GAP, (z0 - half_gap, z1 + half_gap)) for z0, z1 in other
    ]
    leaf += [_knuckle(HINGE_AXIS, HINGE_KNUCKLE_RADIUS, z) for z in own]
    return leaf - _knuckle(HINGE_AXIS, HINGE_PIN_DIAMETER / 2, hinge_z_range(center_z))
