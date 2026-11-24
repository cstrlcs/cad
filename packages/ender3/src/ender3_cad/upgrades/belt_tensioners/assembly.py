from build123d import Compound, Location, Part, Pos

from ender3_cad.dimensions import FACE_BACK, FACE_RIGHT
from ender3_cad.upgrades.belt_tensioners.belt_tensioner_knob import belt_tensioner_knob
from ender3_cad.upgrades.belt_tensioners.belt_tensioner_puller import belt_tensioner_puller
from ender3_cad.upgrades.belt_tensioners.construction import end_wall_u_range
from ender3_cad.upgrades.belt_tensioners.dimensions import (
    IDLER_GAP,
    X_IDLER_TRAVEL,
    X_TENSIONER_LOCATION,
    Y_IDLER_TRAVEL,
    Y_TENSIONER_LOCATION,
)
from ender3_cad.upgrades.belt_tensioners.idler_bushing import idler_bushing
from ender3_cad.upgrades.belt_tensioners.x_belt_tensioner_body import x_belt_tensioner_body
from ender3_cad.upgrades.belt_tensioners.y_belt_tensioner_body import y_belt_tensioner_body


def _tensioner_assembly(label: str, body: Part, location: Location, travel: tuple[float, float]) -> Compound:
    end_wall = end_wall_u_range(travel)
    puller = location * belt_tensioner_puller()
    puller.label = f"{label}_puller"
    knob = location * Pos(end_wall[1], 0, 0) * FACE_RIGHT * belt_tensioner_knob()
    knob.label = f"{label}_knob"
    bushing = location * Pos(0, -IDLER_GAP / 2, 0) * FACE_BACK * idler_bushing()
    bushing.label = f"{label}_idler_bushing"
    return Compound(label=label, children=[body, puller, knob, bushing])


def x_belt_tensioner_assembly() -> Compound:
    return _tensioner_assembly("x_belt_tensioner", x_belt_tensioner_body(), X_TENSIONER_LOCATION, X_IDLER_TRAVEL)


def y_belt_tensioner_assembly() -> Compound:
    return _tensioner_assembly("y_belt_tensioner", y_belt_tensioner_body(), Y_TENSIONER_LOCATION, Y_IDLER_TRAVEL)
