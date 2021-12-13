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

def parse_config(config):
    team_players = config['team_players']
    team_players_ai = config['team_players_ai']
    ind_players = config['ind_players']
    ind_players_ai = config['ind_players_ai']

    team_atom = team_players[0] | team_players[1]
    players = list(sorted(team_players + ind_players, key=lambda x: x.value))
    init_atoms = []
    for p in players:
        if p in team_atom:
            init_atoms.append(team_atom)
        else:
            init_atoms.append(p)

    zipped_team = list(zip(team_players, team_players_ai))
    zipped_ind = list(zip(ind_players, ind_players_ai))

    comb = list(sorted(zipped_team + zipped_ind, key=lambda x: x[0].value))
    players = [a for a, _ in comb]
    agent_ai = [b for _,b in comb]

    return players, agent_ai, init_atoms, team_players, ind_players

def run_experiments(pool, config, num_simulations):

    players, agent_ai, init_atoms, team_players, ind_players = parse_config(config)

    part_func = partial(simulate_game, agent_ai, init_atoms)
    sims = pool.map(part_func, range(num_simulations))
    sims = [list(map(convert, history)) for history in sims]

    team_win_together = team_win_together_stats(sims, team_players)
    team_loose_together = team_loose_together_stats(sims, ind_players)
    team_individual_only_win = team_individual_only_win_stats(sims, team_players)
    return team_win_together, team_loose_together, team_individual_only_win


