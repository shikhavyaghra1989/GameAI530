from enum import IntEnum, Flag, auto

import numpy as np
import numba

class Three_Players(Flag):
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
        assert self != Three_Players.P0 
        if self == Three_Players.P1: return Three_Players.P2
        if self == Three_Players.P2: return Three_Players.P3
        if self == Three_Players.P3: return Three_Players.P1

    def is_union_player(self):
        return ( 
            self == Three_Players.P12 or
            self == Three_Players.P23 or
            self == Three_Players.P13
        )

    def get_union_player_members(self):
        if self == Three_Players.P12: return (Three_Players.P1, Three_Players.P2)
        if self == Three_Players.P23: return (Three_Players.P2, Three_Players.P3)
        if self == Three_Players.P13: return (Three_Players.P1, Three_Players.P3)
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
            if p & Three_Players.P1.value: utilities[0] += 1.0
            if p & Three_Players.P2.value: utilities[1] += 1.0
            if p & Three_Players.P3.value: utilities[2] += 1.0
                
    return utilities