from chainreaction.game import *
from chainreaction.positions import *
from chainreaction.board import *
from chainreaction.four_players import *
from chainreaction.mcts import *
from chainreaction.minimax import *

from experiments.utils import *


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


def run_experiments(pool, num_simulations):
    players = [FourPlayers.P1, FourPlayers.P2, FourPlayers.P3, FourPlayers.P4]
    agent_ai = [minimax_step, mcts_step, minimax_step, mcts_step]
    init_atoms = [FourPlayers.P1, FourPlayers.P2, FourPlayers.P3, FourPlayers.P4]
    
    part_func = partial(simulate_game, agent_ai, init_atoms)
    sims = pool.map(part_func, range(num_simulations))
    sims = [list(map(convert, history)) for history in sims]

    for player, agent_ai in zip(players, agent_ai):
        num_wins = get_win_stats(sims, player)
        print(agent_ai.__name__, num_wins)


