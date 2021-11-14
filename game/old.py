# import numpy as np
# import numba

# from config import *
# from board import *
# from game import *

# def minimax_game(state: Board, curr_player):
#     utilities = board_utility(state.atom_type)
#     while not is_terminal(state.atom_type):
#         curr_player_idx = curr_player.get_zero_indexed_player_idx()

#         if utilities[curr_player_idx] == 0:
#             curr_player = curr_player.next_player()

#         else:
#             pred_utility, move = minimax_step(state.get_copy(), deepcopy(curr_player), 0)

#             atom = Three_Players(state.atom_type[move[0], move[1]])
#             rand_player = curr_player
#             if atom.is_union_player():
#                 choice = np.random.choice(3, 1, p=[0.6, 0.2, 0.2])[0]
#                 # print(choice)
#                 if choice != 0:
#                     players = atom.get_union_player_members()
#                     rand_player = players[choice - 1]
#                     state.atom_type[move[0], move[1]] = rand_player.value
#                     # curr_player = player


#             state = do_move(state, move[0], move[1], rand_player)
#             utilities = board_utility(state.atom_type)
#             print(print_board(state), utilities, curr_player, move)
#             print('----------------')
#             curr_player = curr_player.next_player()

#     print(board_utility(state.atom_type))
