from enum import Flag, auto

import numba
import numpy as np


class ThreePlayers(Flag):
    P0 = 0
    P1 = auto()
    P2 = auto()
    P3 = auto()

    # combinations
    P12 = P1 | P2
    P23 = P2 | P3
    P13 = P1 | P3

    def get_zero_indexed_player_idx(self):
        return self.value.bit_length() - 1

    def next_player(self):
        assert self != ThreePlayers.P0
        if self == ThreePlayers.P1:
            return ThreePlayers.P2
        if self == ThreePlayers.P2:
            return ThreePlayers.P3
        if self == ThreePlayers.P3:
            return ThreePlayers.P1

    def is_union_player(self):
        return (
                self == ThreePlayers.P12 or
                self == ThreePlayers.P23 or
                self == ThreePlayers.P13
        )

    def get_union_player_members(self):
        if self == ThreePlayers.P12:
            return ThreePlayers.P1, ThreePlayers.P2
        if self == ThreePlayers.P23:
            return ThreePlayers.P2, ThreePlayers.P3
        if self == ThreePlayers.P13:
            return ThreePlayers.P1, ThreePlayers.P3
        return None

    @staticmethod
    def num_players():
        return 3


@numba.njit
def three_player_utility(atom_type_board):
    utilities = np.zeros(3, dtype=np.float32)
    for i in range(atom_type_board.shape[0]):
        for j in range(atom_type_board.shape[1]):
            p = atom_type_board[i, j]
            if p & ThreePlayers.P1.value:
                utilities[0] += 1.0
            if p & ThreePlayers.P2.value:
                utilities[1] += 1.0
            if p & ThreePlayers.P3.value:
                utilities[2] += 1.0

    return utilities
