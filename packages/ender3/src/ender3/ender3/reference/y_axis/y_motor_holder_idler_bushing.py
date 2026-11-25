from build123d import Part, Pos

from ender3.ender3.reference.y_axis.construction import stock_idler_bushing

Y_MOTOR_HOLDER_IDLER_BUSHING_LENGTH = 21.0
Y_MOTOR_HOLDER_IDLER_BUSHING_LOCATION = Pos(-5.5, 140.0, 68.0)


def y_motor_holder_idler_bushing() -> Part:
    return stock_idler_bushing(
        Y_MOTOR_HOLDER_IDLER_BUSHING_LENGTH, Y_MOTOR_HOLDER_IDLER_BUSHING_LOCATION, "y_motor_holder_idler_bushing"
    )
