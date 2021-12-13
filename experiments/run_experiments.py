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

from experiments.utils import *

from tqdm import tqdm


from experiments import ai_comparison_experiments




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
    init_atoms = [FourPlayers.P12, FourPlayers.P12, FourPlayers.P3, FourPlayers.P4]
    team = [FourPlayers.P1, FourPlayers.P2]
    ind = [FourPlayers.P3, FourPlayers.P4]

    player_ai_funcs = [minimax_step, minimax_step, minimax_step, minimax_step]
    part_func = partial(simulate_game, player_ai_funcs, init_atoms)
    sims_minimax = pool.map(part_func, range(num_simulations))
    sims_minimax = [list(map(convert, history)) for history in sims_minimax]

    player_ai_funcs = [mcts_step, mcts_step, mcts_step, mcts_step]
    part_func = partial(simulate_game, player_ai_funcs, init_atoms)
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
    ai_comparison_experiments.run_experiments(pool, 100)

    # run_experiments(pool, 100)

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