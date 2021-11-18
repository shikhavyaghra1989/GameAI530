from flask import Flask, jsonify, request
from flask import render_template

from copy import deepcopy
from chainreaction.minimax import *

app = Flask(__name__)
state = Board(3, 3)
current_player = "player1"
players_details = dict()


@app.route("/next_state", methods=['POST'])
def next_state():
    """
    :accepts move: Move made by player. Example: 1,2
    :return: JSON with game status, winner name and new board state
    """
    global players_details, state, current_player
    move = tuple(request.form['move'].split(","))

    if current_player != "player4":
        _, move = minimax_step(state.get_copy(), deepcopy(players_details[current_player]), 0)
    print(f'{current_player} placing on {move}')
    state, player, utilities, terminal = game_step(state, players_details[current_player], move)
    print("New State:")
    print(format_board(state))
    if terminal:
        max_value = max(utilities)
        won_players = [i + 1 for i, j in enumerate(utilities) if j == max_value]
        body = {
            'is_completed': 1,
            'winners': won_players,
            'board_state': str(format_board(state))
        }
    else:
        body = {
            'is_completed': 0,
            'winners': "",
            'board_state': str(format_board(state))
        }
    return jsonify(body)


@app.route("/play", methods=['POST'])
def play():
    """
    :accepts w: width of board
    :accepts h: players of board
    :accepts players: A comma separated string of player names
    :return: JSON with game status, next player name and new board state
    """
    global players_details, state, current_player

    w = request.form['w']
    h = request.form['h']
    players = [FourPlayers.P1, FourPlayers.P2, FourPlayers.P3, FourPlayers.P4]
    player_names = request.form['players'].split(",")
    players_details = dict(zip(player_names, players))

    state = Board(w, h)
    state.place_atom(0, 0, FourPlayers.P1.value)
    state.place_atom(0, w-1, FourPlayers.P23.value)
    state.place_atom(h-1, 0, FourPlayers.P32.value)
    current_player = player_names[3]
    print("Initial State:")
    print(format_board(state))
    body = {
        'is_completed': 0,
        'next_player': player_names[3],
        'board_state': str(format_board(state))
    }
    return jsonify(body)


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
