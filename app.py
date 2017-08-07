from flask import Flask, render_template, jsonify, request
from game import Agent, emptyboard, gameover, NAMES,  BOARD_SIZE, printboard
import pickle

app = Flask(__name__)

# a1 = Agent(1, lossval=-1)
a2 = Agent(-1, lossval=-1)
'''
with open('gameX1.pickle', 'rb') as handle:
    c = pickle.load(handle)
a1.values = c
'''
with open('gameO4.pickle', 'rb') as handle:
    c = pickle.load(handle)
a2.values = c


@app.route('/')
def index():
    return render_template('index.html')


def is_board_full(state):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i][j] == 0:
                return False
    return True


@app.route('/move', methods=['POST'])
def move():
    a1 = Agent(-1, lossval=-1)
    post = request.get_json()
    board = post.get('board')
    chance = post.get('chance')
    state = emptyboard()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                state[i][j] = 0
            elif board[i][j] == 'X':
                state[i][j] = 1
            else:
                state[i][j] = -1

    player = post.get('player')
    computer = post.get('computer')

    # print board,player,computer
    winner = gameover(state)
    #print("check here",winner)
    # Check if player won
    if winner == 2:
        return jsonify(tied = True, computer_wins = False, player_wins = False, board = board)
    elif NAMES[winner] == player:
        return jsonify(tied = False, computer_wins = False, player_wins = True, board = board)

    #print chance
    #print state

    if chance:
        #print 'Using O pickle'
        computer_move = a2.action(state)
    else:
        #print 'Using O pickle'
        computer_move = a2.action(state)

    #print computer_move,computer
    # Make the next move
    board[computer_move[0]][computer_move[1]] = computer
    state[computer_move[0]][computer_move[1]] = -1
    winner = gameover(state)

    #print("check comp",winner)
    # Check if computer won
    if winner == 2:
        return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                      computer_wins = False, player_wins = False, tied=True, board=board)
    # Check if game is over
    elif NAMES[winner] == computer:
        return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                       computer_wins = True, player_wins = False, tied=False, board = board)
    # Game still going
    return jsonify(computer_row = computer_move[0], computer_col = computer_move[1],
                   computer_wins = False, player_wins = False, board = board)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8081)
