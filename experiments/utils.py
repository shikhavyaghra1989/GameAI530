import numpy as np

from multiprocessing import Pool
from functools import partial
import random
import math
import numba
from copy import deepcopy

from chainreaction.game import *
from chainreaction.positions import *
from chainreaction.board import *
from chainreaction.four_players import *

def get_fresh_board(atom_order):
    w, h = 3, 3
    state = Board(w, h)
    state.place_atom(0, 0, atom_order[0].value)
    state.place_atom(0, 2, atom_order[1].value)
    state.place_atom(2, 2, atom_order[2].value)
    state.place_atom(2, 0, atom_order[3].value)
    return state


def simulate_game(player_ai_funcs, init_atoms, n=0):
    state = get_fresh_board(init_atoms)
    history = []
    player = deepcopy(FourPlayers.P1)
    temp_player = player
    moves_count = 0
    while True:
        before = state.get_copy()
        curr_player = deepcopy(player)
        ai_func = player_ai_funcs[curr_player.get_zero_indexed_player_idx()]
        _, move = ai_func(state.get_copy(), deepcopy(player), 0)
        moves_count += 1
        state, player, utilities, terminal = game_step(state, player, move)
        after = state.get_copy()
        history.append((before._data, after._data, curr_player))
        if terminal and moves_count>4:
            max_value = max(utilities)
            won_players = [i+1 for i, j in enumerate(utilities) if j == max_value]
            break

        temp_player = player
    return history

def convert(data):
    before, after, player = data
    before_board = Board(3, 3)
    before_board._data[:] = before
    after_board = Board(3, 3)
    after_board._data[:] = after
    return (before_board, after_board, player)