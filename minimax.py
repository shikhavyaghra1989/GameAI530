import numpy as np
import numba

from config import *
from board import *
from game import *

def minimax_step(curr_state: Board, curr_player: Players, depth: int):
    
    utilities = board_utility(curr_state.atom_type)
    if is_terminal(curr_state.atom_type):
        return utilities, None

    if depth > 3:
        return board_utility(curr_state.atom_type), None
    
    curr_player_idx = curr_player.get_zero_indexed_player_idx()
    
    if utilities[curr_player_idx] == 0:
        # the player has no more atoms he can control
        # proceed onto the next player in the tree
        # do not increase the depth
        return minimax_step(curr_state, curr_player.next_player(), depth + 1)

    max_player_utility = -1 * np.inf
    max_utilities = None
    best_move = None
    temp_state = curr_state.get_copy()

    curr_player_moves = allowed_moves(curr_state, curr_player)
    for i in range(curr_player_moves[0].shape[0]):
        row_idx = curr_player_moves[0][i]
        col_idx = curr_player_moves[1][i]

        atom = Players(temp_state.atom_type[row_idx, col_idx])
        if atom.is_union_player():
            P_a, P_b = atom.get_union_player_members()
            avg_utilities = np.zeros(Players.num_players())

            # map out the possibilities
            # no change
            next_state = do_move(temp_state.get_copy(), row_idx, col_idx, curr_player)
            utility, move = minimax_step(next_state, curr_player.next_player(), depth + 1)
            avg_utilities += 0.6 * utility

            # P_a change
            next_state = temp_state.get_copy()
            next_state.atom_type[row_idx, col_idx] = P_a.value
            next_state = do_move(next_state, row_idx, col_idx, P_a)
            utility, move = minimax_step(next_state, curr_player.next_player(), depth + 1)
            avg_utilities += 0.2 * utility

            # P_b change
            next_state = temp_state.get_copy()
            next_state.atom_type[row_idx, col_idx] = P_b.value
            next_state = do_move(next_state, row_idx, col_idx, P_b)
            utility, move = minimax_step(next_state, curr_player.next_player(), depth + 1)
            avg_utilities += 0.2 * utility

            if avg_utilities[curr_player_idx] > max_player_utility:
                max_player_utility = utilities[curr_player_idx]
                max_utilities = utility
                best_move = (row_idx, col_idx)

        else:
            next_state = do_move(temp_state, row_idx, col_idx, curr_player)
            utility, move = minimax_step(next_state, curr_player.next_player(), depth + 1)
            if utilities[curr_player_idx] > max_player_utility:
                max_player_utility = utilities[curr_player_idx]
                max_utilities = utility
                best_move = (row_idx, col_idx)

        # reset
        Board.copy_from_to(curr_state, temp_state)

    # assert best_move is not None
    return max_utilities, best_move




    