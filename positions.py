from enum import IntEnum, Flag, auto


class Positions(IntEnum):
    # corner positions
    TOP_LEFT_CORNER = auto()
    TOP_RIGHT_CORNER = auto()
    BOTTOM_LEFT_CORNER = auto()
    BOTTOM_RIGHT_CORNER = auto()

    # side positions
    LEFT_SIDE = auto()
    RIGHT_SIDE = auto()
    TOP_SIDE = auto()
    BOTTOM_SIDE = auto()

    # remaining position
    INSIDE = auto()
