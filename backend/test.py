import requests
import json

base_url = 'http://localhost:5000'  # Replace with your actual URL

# Test for a valid move
valid_move_data = {'position': 0, 'player': 'X'}
response = requests.post(f'{base_url}/make_move', json=valid_move_data)
print(response.status_code)  # Should be 200 for success

# Test for an invalid move
invalid_move_data = {'position': 0, 'player': 'O'}  # Trying to overwrite a move
response = requests.post(f'{base_url}/make_move', json=invalid_move_data)
print(response.status_code)  # Should be an error code

# Test for winning move (adjust moves to create a win)
winning_moves = [{'position': 0, 'player': 'X'}, {'position': 1, 'player': 'O'},
                 {'position': 3, 'player': 'X'}, {'position': 4, 'player': 'O'},
                 {'position': 6, 'player': 'X'}]
for move in winning_moves:
    response = requests.post(f'{base_url}/make_move', json=move)
print(response.status_code)  # Should be 200
print(response.json())  # Verify that the winner is correctly identified

# Test for a draw (adjust moves to create a draw)
draw_moves = [{'position': 0, 'player': 'X'}, {'position': 1, 'player': 'O'},
              {'position': 2, 'player': 'X'}, {'position': 4, 'player': 'O'},
              {'position': 3, 'player': 'X'}, {'position': 5, 'player': 'O'},
              {'position': 6, 'player': 'O'}, {'position': 7, 'player': 'X'},
              {'position': 8, 'player': 'O'}]
for move in draw_moves:
    response = requests.post(f'{base_url}/make_move', json=move)
print(response.status_code)  # Should be 200
print(response.json())  # Verify that a draw is correctly identified

# Add more tests for AI moves, real-time communication, and resetting the game
