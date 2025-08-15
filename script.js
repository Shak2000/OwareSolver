// This file connects the Oware game UI to the FastAPI backend using fetch().
// It handles game state updates, user interactions, and displaying the board.

document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const boardHouses = Array.from(document.querySelectorAll('.house'));
    const topScoreElement = document.getElementById('top-score');
    const bottomScoreElement = document.getElementById('bottom-score');
    const playerTurnElement = document.getElementById('player-turn');
    const startGameBtn = document.getElementById('start-game-btn');
    const undoBtn = document.getElementById('undo-btn');
    const aiMoveBtn = document.getElementById('ai-move-btn');
    const depthInput = document.getElementById('depth-input');

    // API calls
    const API_URL = window.location.origin;

    // State variable to track if the AI is thinking
    let isThinking = false;

    /**
     * Fetches the current game state (board, scores, player) from the server.
     * @returns {Promise<object>} The game state.
     */
    async function getGameState() {
        try {
            const response = await fetch(`${API_URL}/get_game_state`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching game state:', error);
            return null;
        }
    }

    /**
     * Updates the UI with the current game state.
     * @param {object} gameState - The current game state.
     */
    function updateUI(gameState) {
        if (!gameState) {
            return;
        }

        // Update scores
        topScoreElement.textContent = gameState.top;
        bottomScoreElement.textContent = gameState.bottom;

        // Update houses with bead counts
        gameState.board.forEach((beads, index) => {
            const houseElement = boardHouses.find(h => parseInt(h.dataset.houseId) === index);
            if (houseElement) {
                houseElement.textContent = beads;
            }
        });

        // Update player turn message
        playerTurnElement.textContent = `Current Player: ${gameState.player === 'T' ? 'Top' : 'Bottom'}`;

        // Disable buttons and houses if AI is thinking or a winner exists
        const disableAll = isThinking || !!gameState.winner;
        undoBtn.disabled = disableAll || gameState.history_length === 0;
        aiMoveBtn.disabled = disableAll;
        startGameBtn.disabled = isThinking;
        depthInput.disabled = isThinking;

        boardHouses.forEach(house => {
            const isClickable = !disableAll;
            house.style.cursor = isClickable ? 'pointer' : 'not-allowed';
            if (isClickable) {
                house.classList.add('active');
            } else {
                house.classList.remove('active');
            }
        });

        // Check for winner
        if (gameState.winner) {
            playerTurnElement.textContent = `Game Over! Winner is ${gameState.winner === 'Tie' ? 'Tie' : gameState.winner === 'T' ? 'Top Player' : 'Bottom Player'}.`;
            aiMoveBtn.disabled = true;
            undoBtn.disabled = true;
            startGameBtn.disabled = false;
        }
    }

    /**
     * Starts a new game by calling the server endpoint.
     */
    async function startGame() {
        try {
            await fetch(`${API_URL}/start`, { method: 'POST' });
            const newState = await getGameState();
            updateUI(newState);
            console.log('New game started.');
        } catch (error) {
            console.error('Error starting new game:', error);
        }
    }

    /**
     * Undoes the last move.
     */
    async function undoMove() {
        try {
            await fetch(`${API_URL}/undo`, { method: 'POST' });
            const newState = await getGameState();
            updateUI(newState);
            console.log('Last move undone.');
        } catch (error) {
            console.error('Error undoing move:', error);
        }
    }

    /**
     * Executes a player's move.
     * @param {number} houseId - The 0-based index of the house.
     */
    async function makeMove(houseId) {
        if (isThinking) return;

        try {
            const response = await fetch(`${API_URL}/move/${houseId}`, { method: 'POST' });
            const success = await response.json();
            if (success) {
                const newState = await getGameState();
                updateUI(newState);
                // Switch player turn after a successful move
                await fetch(`${API_URL}/switch`, { method: 'POST' });
                const finalState = await getGameState();
                updateUI(finalState);
                console.log(`Player moved from house ${houseId}`);
            } else {
                console.log('Invalid move.');
            }
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    /**
     * Triggers an AI move.
     */
    async function makeAIMove() {
        if (isThinking) return;

        isThinking = true;
        updateUI(await getGameState()); // Update UI to reflect thinking state

        try {
            const depth = depthInput.value;
            // The AI move logic is a bit more complex in your main.py, it finds the best move and
            // then calls game.move(). We'll call the ai_move endpoint which should handle this.
            await fetch(`${API_URL}/ai_move/${depth}`, { method: 'POST' });
            const newState = await getGameState();
            updateUI(newState);
            console.log('AI made a move.');
        } catch (error) {
            console.error('Error making AI move:', error);
        } finally {
            isThinking = false;
            updateUI(await getGameState()); // Final update to re-enable controls
        }
    }

    // Event listeners
    startGameBtn.addEventListener('click', startGame);
    undoBtn.addEventListener('click', undoMove);
    aiMoveBtn.addEventListener('click', makeAIMove);

    boardHouses.forEach(house => {
        house.addEventListener('click', () => {
            if (isThinking) return;

            const houseId = parseInt(house.dataset.houseId);
            // We need to determine the player and their corresponding house numbers.
            // The API move() method takes 1-6 as input, not the 0-11 index.
            // Houses 0-5 are for the bottom player (input 1-6)
            // Houses 6-11 are for the top player (input 1-6)
            // We need to fetch the current player to determine the correct house number for the API call.
            getGameState().then(state => {
                if (state.player === 'B' && houseId >= 0 && houseId <= 5) {
                    const apiHouseNumber = houseId + 1;
                    makeMove(apiHouseNumber);
                } else if (state.player === 'T' && houseId >= 6 && houseId <= 11) {
                    const apiHouseNumber = houseId - 5;
                    makeMove(apiHouseNumber);
                } else {
                    console.log("It's not your turn or you clicked on an invalid house.");
                }
            });
        });
    });

    // Initial state setup on page load
    async function getInitialState() {
        const response = await fetch(`${API_URL}/get_game_state`);
        const data = await response.json();
        updateUI(data);
    }

    getInitialState();
});
