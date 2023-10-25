import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [currentPlayer, setCurrentPlayer] = useState('X');
  const [winner, setWinner] = useState(null);
  const [draw, setDraw] = useState(false);

  const handleCellClick = (index) => {
    if (!board[index] && !winner) {
      // Update the local state to show the move instantly
      const updatedBoard = [...board];
      updatedBoard[index] = currentPlayer;
      setBoard(updatedBoard);

      // Send the move to the backend (you should implement this)
      sendMoveToBackend(index, currentPlayer);
    }
  };

  const sendMoveToBackend = (position, player) => {
    // Send a POST request to your Flask backend to make the move
    fetch('/make_move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ position, player }),
    })
      .then((response) => {
        if (response.status === 200) {
          // Move was successful, update the game state if needed
          // You can update the game state when you receive a response from the backend
        } else {
          // Handle error, move not accepted
          console.error('Move not accepted by the backend.');
        }
      })
      .catch((error) => {
        // Handle network error
        console.error('Network error:', error);
      });
  };
  

  useEffect(() => {
    const fetchGameState = async () => {
      try {
        const response = await fetch('/get_game_state'); // Adjust the endpoint as needed
        if (response.status === 200) {
          const data = await response.json();
          // Update the game state based on the data received from the backend
          setBoard(data.board);
          setCurrentPlayer(data.current_player);
          setWinner(data.winner);
          setDraw(data.draw);
        } else {
          console.error('Failed to fetch game state from the backend.');
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    };
  
    // Fetch the game state initially and set up periodic updates (adjust the interval as needed)
    fetchGameState();
    const intervalId = setInterval(fetchGameState, 1000); // Example: Fetch every second
  
    return () => {
      clearInterval(intervalId);
    };
  }, []); // This effect runs once when the component mounts
  

  // Implement a function to reset the game and send a reset request to the backend
  const resetGame = () => {
    fetch('/reset_game', {
      method: 'POST',
    })
      .then((response) => {
        if (response.status === 200) {
          // Reset the game state in the frontend
          setBoard(Array(9).fill(null));
          setCurrentPlayer('X');
          setWinner(null);
          setDraw(false);
        } else {
          console.error('Failed to reset the game on the backend.');
        }
      })
      .catch((error) => {
        console.error('Network error:', error);
      });
  };
  

  return (
    <div className="App">
      <h1>Tic Tac Toe</h1>
      <div className="board">
        {board.map((cell, index) => (
          <div
            key={index}
            className="cell"
            onClick={() => handleCellClick(index)}
          >
            {cell}
          </div>
        ))}
      </div>
      {winner && <p>{winner} wins!</p>}
      {draw && <p>It's a draw!</p>}
      {!winner && !draw && <p>Current player: {currentPlayer}</p>}
      <button onClick={resetGame}>Reset Game</button>
    </div>
  );
}

export default App;
