from flask import Flask
from flask import render_template

from copy import deepcopy
from game.minimax import *

app = Flask(__name__)


@app.route("/")
def next_state(state, player, move=None):
    if player != "4":
        _, move = minimax_step(state.get_copy(), deepcopy(player), 0)
    print(f'{player} placing on {move}')
    state, player, utilities, terminal = game_step(state, player, move)
    print("New State:")
    print(format_board(state))
    if terminal:
        max_value = max(utilities)
        won_players = [i + 1 for i, j in enumerate(utilities) if j == max_value]
        return "completed", won_players
    else:
        return state, format_board(state)


@app.route("/")
def play(w, h):
    state = Board(w, h)
    state.place_atom(0, 0, FourPlayers.P1.value)
    state.place_atom(0, 2, FourPlayers.P23.value)
    state.place_atom(2, 0, FourPlayers.P32.value)
    print("Initial State:")
    print(format_board(state))
    return state, format_board(state)


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
