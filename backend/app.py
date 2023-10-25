from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the game state
game_state = {
    'board': [None] * 9,  # Represents a 3x3 board
    'current_player': 'X',  # Player X starts
    'winner': None,
    'draw': False,
}

# Check for a win
def check_win(player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in win_combinations:
        if all(game_state['board'][i] == player for i in combo):
            return True
    return False

# Check for a draw
def check_draw():
    return all(cell is not None for cell in game_state['board'])

# AI for single-player (Minimax algorithm)
def minimax(player):
    # Maximizer's turn
    if player == 'O':
        best_score = -float('inf')
        best_move = None

        for i in range(9):
            if game_state['board'][i] is None:
                game_state['board'][i] = 'O'
                score = minimax('X')
                game_state['board'][i] = None

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    # Minimizer's turn
    else:
        best_score = float('inf')

        for i in range(9):
            if game_state['board'][i] is None:
                game_state['board'][i] = 'X'
                score = minimax('O')
                game_state['board'][i] = None

                if score < best_score:
                    best_score = score

        return best_score

# Flask route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Flask-SocketIO events
@socketio.on('make_move')
def handle_move(data):
    position = data['position']
    player = data['player']
    
    if game_state['board'][position] is None and game_state['current_player'] == player and not game_state['winner']:
        game_state['board'][position] = player

        if check_win(player):
            game_state['winner'] = player
        elif check_draw():
            game_state['draw'] = True
        else:
            game_state['current_player'] = 'O' if player == 'X' else 'X'

        emit('update_game', game_state, broadcast=True)

@socketio.on('reset_game')
def reset_game():
    global game_state
    game_state = {
        'board': [None] * 9,
        'current_player': 'X',
        'winner': None,
        'draw': False,
    }
    emit('update_game', game_state, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
