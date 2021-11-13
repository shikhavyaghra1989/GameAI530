from positions import Positions
import config

import numpy as np
import numba
import random

@numba.njit
def get_position(i: int, j: int, width: int, height: int):
    # check if inside
    if i > 0 and j > 0 and i < width - 1 and j < height - 1: return Positions.INSIDE

    left = False
    right = False
    top = False
    bottom = False

    if i == 0: top = True
    if i == width - 1: bottom = True

    if j == 0: left = True
    if j == height - 1: right = True

    # corners
    if left is True and top is True: return Positions.TOP_LEFT_CORNER
    if right is True and top is True: return Positions.TOP_RIGHT_CORNER
    if left is True and bottom is True: return Positions.BOTTOM_LEFT_CORNER
    if right is True and bottom is True: return Positions.BOTTOM_RIGHT_CORNER

    # sides
    if left is True and (top is False and bottom is False): return Positions.LEFT_SIDE
    if right is True and (top is False and bottom is False): return Positions.RIGHT_SIDE
    if top is True and (left is False and right is False): return Positions.TOP_SIDE
    if bottom is True and (left is False and right is False): return Positions.BOTTOM_SIDE

spec = [
    ('width', numba.uint8),
    ('height', numba.uint8),
    ('_data', numba.uint8[:, :, :]),
    ('atom_count', numba.uint8[:, :]),
    ('atom_type', numba.uint8[:, :])
]
@numba.experimental.jitclass(spec)
class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._data = np.zeros((2, height, width), dtype=np.uint8)
        self.atom_count = self._data[0]
        self.atom_type = self._data[1]

    @staticmethod
    def copy_from_to(A, B):
        B._data[:] = A._data

    def get_copy(self):
        ret = Board(self.width, self.height)
        ret._data[:] = self._data
        return ret

    def place_atom(self, i, j, atom_type):
        self.atom_count[i, j] += 1
        self.atom_type[i, j] = atom_type

    def clear_cell(self, i, j):
        self.atom_count[i, j] = 0
        self.atom_type[i, j] = 0

    def check_explosion(self, i, j):
        # Check if the current number of atoms at position (i,j) exceeded limit
        width = self.width
        height = self.height
        position = get_position(i, j, width, height)
        num_atoms = self.atom_count[i, j]

        # check corners
        if (position == Positions.TOP_LEFT_CORNER or 
            position == Positions.TOP_RIGHT_CORNER or 
            position == Positions.BOTTOM_LEFT_CORNER or 
            position == Positions.BOTTOM_RIGHT_CORNER ):

            # assert num_atoms <= 2
            if num_atoms >= 2:
                return True
            else:
                return False

        # check sides
        if (position == Positions.TOP_SIDE or 
            position == Positions.BOTTOM_SIDE or 
            position == Positions.LEFT_SIDE or 
            position == Positions.RIGHT_SIDE):

            # assert num_atoms <= 3
            if num_atoms >= 3:
                return True
            else:
                return False

        # check inside
        if position == Positions.INSIDE:
            # assert num_atoms <= 4
            if num_atoms >= 4:
                return True
            else:
                return False

    def explode(self, i, j):
        # During an explosion, the current cell is made as zero
        # Depending on the position (i, j), neighbouring cells are affected
        # It returns a list of indices where eacj (i,j) represents the affected neighbours
        width = self.width
        height = self.height
        position = get_position(i, j, width, height)
        atom_type = self.atom_type[i, j]

        self.clear_cell(i, j)

        # handle corners
        if position == Positions.TOP_LEFT_CORNER:
            self.place_atom(i + 1, j, atom_type)
            self.place_atom(i, j + 1, atom_type)
            return [(i + 1, j), (i, j + 1)]
            
        if position == Positions.TOP_RIGHT_CORNER:
            self.place_atom(i, j - 1, atom_type)
            self.place_atom(i + 1, j, atom_type)
            return [(i, j - 1), (i + 1, j)]

        if position == Positions.BOTTOM_LEFT_CORNER:
            self.place_atom(i, j + 1, atom_type)
            self.place_atom(i - 1, j, atom_type)
            return [(i, j + 1), (i - 1, j)]

        if position == Positions.BOTTOM_RIGHT_CORNER:
            self.place_atom(i, j - 1, atom_type)
            self.place_atom(i - 1, j, atom_type)
            return [(i, j - 1), (i - 1, j)]

        # handle sides
        if position == Positions.TOP_SIDE:
            self.place_atom(i, j - 1, atom_type)
            self.place_atom(i + 1, j, atom_type)
            self.place_atom(i, j + 1, atom_type)
            return [(i, j - 1), (i + 1, j), (i, j + 1)]

        if position == Positions.BOTTOM_SIDE:
            self.place_atom(i, j - 1, atom_type)
            self.place_atom(i, j + 1, atom_type)
            self.place_atom(i - 1, j, atom_type)
            return [(i, j - 1), (i, j + 1), (i - 1, j)]

        if position == Positions.LEFT_SIDE:
            self.place_atom(i - 1, j, atom_type)
            self.place_atom(i + 1, j, atom_type)
            self.place_atom(i, j + 1, atom_type)
            return [(i - 1, j), (i + 1, j), (i, j + 1)]

        if position == Positions.RIGHT_SIDE:
            self.place_atom(i - 1, j, atom_type)
            self.place_atom(i + 1, j, atom_type)
            self.place_atom(i, j - 1, atom_type)
            return [(i - 1, j), (i + 1, j), (i, j - 1)]

        # handle inside
        if position == Positions.INSIDE:
            self.place_atom(i, j - 1, atom_type)
            self.place_atom(i, j + 1, atom_type)
            self.place_atom(i - 1, j, atom_type)
            self.place_atom(i + 1, j, atom_type)
            return [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]

def print_board(board: Board):
    atom_count_board = board.atom_count.astype(str)
    f = np.vectorize(lambda x: config.Players(x).name)
    players = f(board.atom_type)

    res = np.char.add('-', players)
    res = np.char.add(atom_count_board, res)
    return repr(res)