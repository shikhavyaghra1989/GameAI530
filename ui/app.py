from flask import Flask, jsonify, request
from flask import render_template

from copy import deepcopy
from chainreaction.minimax import *

app = Flask(__name__)
w = 3
h = 3
state = Board(3, 3)
current_player = "player1"
players_details = dict()
# basic colors
# red+blue, yellow+green
# red+yellow, blue+green
# red+green, blue+yellow
# default
colors = ['red', 'blue', 'yellow', 'green',
          'Magenta', 'YellowGreen',
          'orange', 'cyan',
          'LightGrey', 'MediumTurquoise',
          'black']


def make_board_state(new_state):
    global w, h
    row = 0
    col = 0
    board_state = "["
    for item in new_state:
        if item[0].isdigit() or item.startswith('-'):
            col += 1
            if item[3:] == 1:
                color = colors[0]
            elif item[3:] == 2:
                color = colors[1]
            elif item[3:] == 3:
                color = colors[2]
            elif item[3:] == 4:
                color = colors[3]
            elif item[3:] == 12:
                color = colors[4]
            elif item[3:] == 34:
                color = colors[5]
            elif item[3:] == 13:
                color = colors[6]
            elif item[3:] == 24:
                color = colors[7]
            elif item[3:] == 14:
                color = colors[8]
            elif item[3:] == 23:
                color = colors[9]
            else:
                color = colors[10]
            board_state += "(" + str(row) + "," + str(col) + "," + color + ")"
            if col == w:
                row += 1
                col = 0
    board_state += "]"
    return board_state


@app.route("/next_state", methods=["GET", "POST"])
def next_state():
    """
    :accepts move: Move made by player. Example: 1,2
    :return: JSON with game status, winner name and new board state
    """
    global players_details, state, current_player, w, h, colors
    move = tuple(map(int, request.args.get('move').split(",")))

    if current_player != "player4":
        _, move = minimax_step(state.get_copy(), deepcopy(players_details[current_player]), 0)
    print(f'{current_player} placing on {move}')
    state, player, utilities, terminal = game_step(state, players_details[current_player], move)
    print("New State:")
    print(format_board(state))
    new_state = str(str(format_board(state))[1:-1].split(" ")).split("'")
    board_state = make_board_state(new_state)
    if terminal:
        max_value = max(utilities)
        won_players = [i + 1 for i, j in enumerate(utilities) if j == max_value]
        body = {
            'is_completed': 1,
            'winners': won_players,
            'board_state': board_state
        }
    else:
        body = {
            'is_completed': 0,
            'winners': "",
            'board_state': board_state
        }
    return jsonify(body)


@app.route("/play", methods=["GET", "POST"])
def play():
    """
    :accepts w: width of board
    :accepts h: players of board
    :accepts players: A comma separated string of player names
    :return: JSON with game status, next player name and new board state
    """
    global players_details, state, current_player, w, h

    w = int(request.args.get('w'))
    h = int(request.args.get('h'))

    players = [FourPlayers.P1, FourPlayers.P2, FourPlayers.P3, FourPlayers.P4]
    player_names = request.args.get('players').split(",")
    players_details = dict(zip(player_names, players))

    state = Board(w, h)
    state.place_atom(0, 0, FourPlayers.P1.value)
    state.place_atom(0, w-1, FourPlayers.P2.value)
    state.place_atom(h-1, 0, FourPlayers.P3.value)
    current_player = player_names[3]
    print("Initial State:")
    print(format_board(state))
    new_state = str(str(format_board(state))[1:-1].split(" ")).split("'")
    board_state = make_board_state(new_state)
    body = {
        'is_completed': 0,
        'next_player': player_names[3],
        'board_state': board_state
    }
    return jsonify(body)


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5001)
