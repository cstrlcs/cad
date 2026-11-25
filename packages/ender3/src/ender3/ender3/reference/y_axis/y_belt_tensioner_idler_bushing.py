from build123d import Part, Pos

from ender3.ender3.reference.y_axis.construction import stock_idler_bushing

Y_BELT_TENSIONER_IDLER_BUSHING_LENGTH = 40.0
Y_BELT_TENSIONER_IDLER_BUSHING_LOCATION = Pos(0.0, -236.0, 68.0)


def y_belt_tensioner_idler_bushing() -> Part:
    return stock_idler_bushing(
        Y_BELT_TENSIONER_IDLER_BUSHING_LENGTH, Y_BELT_TENSIONER_IDLER_BUSHING_LOCATION, "y_belt_tensioner_idler_bushing"
    )
