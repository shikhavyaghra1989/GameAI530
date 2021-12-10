import numpy as np
from enum import Enum, IntEnum, auto
import typing

from multiprocessing import Pool
from functools import partial
import random
import math
import numba
from copy import deepcopy

from chainreaction.game import *
from chainreaction.positions import *
from chainreaction.board import *
from chainreaction.minimax import *
from chainreaction.mcts import *
from chainreaction.four_players import *

from tqdm import tqdm



def get_fresh_board(atom_order):
    w, h = 3, 3
    state = Board(w, h)
    state.place_atom(0, 0, atom_order[0].value)
    state.place_atom(0, 2, atom_order[1].value)
    state.place_atom(2, 0, atom_order[2].value)
    state.place_atom(2, 2, atom_order[3].value)
    return state


def simulate_game(ai_func, init_atoms, n=0):
    state = get_fresh_board(init_atoms)
    history = []
    player = deepcopy(FourPlayers.P1)
    temp_player = player
    moves_count = 0
    while True:
        before = state.get_copy()
        curr_player = deepcopy(player)
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


def get_win_stats(simulations, player):
    num_wins = 0
    for history in simulations:
        last_state = history[-1][1]
        atom_type_board = last_state.atom_type
        atom_type_board = atom_type_board[atom_type_board > 0]

        atom_types = set([FourPlayers(i) for i in atom_type_board.flat])
        if player in atom_types:
            num_wins += 1

    return num_wins


def team_win_together_stats(simulations, team_players):
    # this gives the total number of games that teamed up players has won as a team
    # i.e, the last ball present in the board is a team ball
    p1 = team_players[0]
    p2 = team_players[1]
    p_team = p1 | p2
    return get_win_stats(simulations, p_team)

def team_loose_together_stats(simulations, single_players):
    p1 = single_players[0]
    p2 = single_players[1]
    return get_win_stats(simulations, p1) + get_win_stats(simulations, p2)

def team_individual_only_win_stats(simulations, team_players):
    p1 = team_players[0]
    p2 = team_players[1]
    return get_win_stats(simulations, p1) + get_win_stats(simulations, p2)




def run_experiments(pool, num_simulations):
    init_atoms = [FourPlayers.P13, FourPlayers.P2, FourPlayers.P13, FourPlayers.P4]
    team = [FourPlayers.P1, FourPlayers.P3]
    ind = [FourPlayers.P2, FourPlayers.P4]

    part_func = partial(simulate_game, minimax_step, init_atoms)
    sims_minimax = pool.map(part_func, range(num_simulations))
    sims_minimax = [list(map(convert, history)) for history in sims_minimax]

    part_func = partial(simulate_game, mcts_step, init_atoms)
    sims_mcts = pool.map(part_func, range(num_simulations))
    sims_mcts = [list(map(convert, history)) for history in sims_mcts]

    print('minimax')
    team_win_together = team_win_together_stats(sims_minimax, team)
    team_loose_together = team_loose_together_stats(sims_minimax, ind)
    team_individual_only_win = team_individual_only_win_stats(sims_minimax, team)
    print(team_win_together, team_loose_together, team_individual_only_win)

    print('mcts')
    team_win_together = team_win_together_stats(sims_mcts, team)
    team_loose_together = team_loose_together_stats(sims_mcts, ind)
    team_individual_only_win = team_individual_only_win_stats(sims_mcts, team)
    print(team_win_together, team_loose_together, team_individual_only_win)
    return None


if __name__ == '__main__':
    pool = Pool(8)
    run_experiments(pool, 100)

    # num_simulations = 100
    # ind_stats = [0, 0, 0, 0]
    # team_stats = 0

    # sim_iter = pool.imap_unordered(simulate_game, range(num_simulations))

    # for history in tqdm(sim_iter):
    #     history = list(map(convert, history))
    #     last_state = history[-1][1]

    #     utilities = board_utility(last_state.atom_type)
    #     max_value = np.max(utilities)
    #     won_players = [i+1 for i, j in enumerate(utilities) if j == max_value]
    #     if len(won_players)==1:
    #         player_id = won_players[0] - 1
    #         ind_stats[player_id] = ind_stats[player_id] + 1
    #     else:
    #         team_stats += 1
    #         # ind_stats[won_players[0] - 1] = ind_stats[won_players[0] - 1] + 1
    #         # ind_stats[won_players[1] - 1] = ind_stats[won_players[1] - 1] + 1

    # print(ind_stats, team_stats)