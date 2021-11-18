"""
@description : Code to test the game
"""
from copy import deepcopy
from minimax import *

w, h = 3, 3
state = Board(w, h)
state.place_atom(0, 0, FourPlayers.P1.value)
state.place_atom(0, 2, FourPlayers.P2.value)
state.place_atom(2, 0, FourPlayers.P34.value)
state.place_atom(2, 2, FourPlayers.P34.value)
moves_count = 0
print("Initial State:")
print(format_board(state))

player = FourPlayers.P1
while True:
    _, move = minimax_step(state.get_copy(), deepcopy(player), 0)
    moves_count += 1
    print(f'{player} placing on {move}')
    state, player, utilities, terminal = game_step(state, player, move)
    print("New State:")
    print(format_board(state))
    if terminal and moves_count > 4:
        max_value = max(utilities)
        won_players = [i+1 for i, j in enumerate(utilities) if j == max_value]
        if len(won_players) == 1:
            print("Game Won by Player " + str(won_players[0]))
        else:
            won_players_ints = [str(i) for i in won_players]
            print("Game Won by Players " + (", ".join(won_players_ints)))
        break
    print('=='*20)
