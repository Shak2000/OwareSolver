# Oware Solver

A complete implementation of the traditional African board game Oware (also known as Awale) with both command-line and web interfaces, featuring an AI opponent powered by the minimax algorithm with alpha-beta pruning.

## Features

- **Two Game Modes**: Command-line interface and modern web UI
- **AI Opponent**: Intelligent computer player with configurable difficulty
- **Move Validation**: Enforces all traditional Oware rules including the "feeding" rule
- **Undo System**: Take back moves to explore different strategies
- **Responsive Design**: Web interface works on desktop and mobile devices
- **Real-time Updates**: Dynamic board updates and game state management

## Game Rules

Oware is played on a board with 12 houses (6 per player) and 48 beads. Each player starts with 4 beads in each of their houses.

### Objective
Capture more than 24 beads to win the game.

### How to Play
1. Players take turns picking up all beads from one of their houses
2. Beads are sown counter-clockwise, one per house
3. If the last bead lands in an opponent's house containing 2 or 3 beads total, capture those beads
4. Continue capturing backwards if consecutive opponent houses also have 2 or 3 beads
5. **Feeding Rule**: If your opponent's side is empty, you must make a move that gives them beads (if possible)

### Winning Conditions
- Capture more than 24 beads
- If no moves are possible, remaining beads are distributed and the player with the most beads wins

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Required Dependencies
```bash
pip install fastapi uvicorn
```

### Setup
1. Clone or download the project files
2. Ensure all files are in the same directory:
   - `main.py` - Core game logic and CLI
   - `app.py` - FastAPI web server
   - `index.html` - Web interface
   - `styles.css` - Styling
   - `script.js` - Frontend JavaScript
   - `README.md` - This file

## Usage

### Web Interface (Recommended)

1. **Start the web server:**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:8000
   ```

3. **Game Controls:**
   - **Start New Game**: Initialize a fresh game
   - **Click Houses**: Click on your houses (bottom row) to make moves
   - **AI Move**: Let the computer make a move with configurable depth (1-15)
   - **Undo**: Take back the last move
   - **Depth Setting**: Adjust AI difficulty (higher = smarter but slower)

### Command Line Interface

Run the CLI version directly:
```bash
python main.py
```

**CLI Commands:**
- `1` - Make a human move
- `2` - Let computer make a move
- `3` - Undo last move
- `4` - Restart game
- `5` - Quit

## AI Difficulty Levels

The AI uses minimax with alpha-beta pruning. Adjust the depth for different difficulty levels:

- **Depth 1-3**: Beginner (very fast)
- **Depth 4-6**: Intermediate (fast)
- **Depth 7-9**: Advanced (moderate speed)
- **Depth 10-12**: Expert (slower)
- **Depth 13-15**: Master (very slow)

## File Structure

```
oware-solver/
├── main.py          # Core game logic and CLI interface
├── app.py           # FastAPI web server and API endpoints
├── index.html       # Web interface HTML
├── styles.css       # Web interface styling
├── script.js        # Frontend JavaScript logic
└── README.md        # This documentation
```

## API Endpoints

The web server provides these REST endpoints:

- `GET /` - Serve the web interface
- `GET /get_game_state` - Get current game state
- `POST /start` - Start a new game
- `POST /move/{house}` - Make a move (house 1-6)
- `POST /ai_move/{depth}` - Trigger AI move with specified depth
- `POST /switch` - Switch current player
- `POST /undo` - Undo last move

## Technical Implementation

### Game Engine
- **Board Representation**: Single array of 12 integers (houses 0-5 for bottom player, 6-11 for top player)
- **Move Validation**: Comprehensive rule enforcement including edge cases
- **State Management**: Complete game state tracking with undo history

### AI Algorithm
- **Minimax**: Game tree search algorithm for optimal play
- **Alpha-Beta Pruning**: Performance optimization to reduce search space
- **Evaluation Function**: Board position scoring based on captured beads

### Web Architecture
- **Backend**: FastAPI for REST API and static file serving
- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **Styling**: Custom CSS with responsive design and smooth animations

## Development Notes

### Game State Format
```python
{
    "board": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],  # 12 houses
    "top": 0,           # Top player score
    "bottom": 0,        # Bottom player score  
    "player": "B",      # Current player ('T' or 'B')
    "history_length": 0, # Number of moves made
    "winner": null      # Winner ('T', 'B', 'Tie', or null)
}
```

### Move Numbering
- **API/CLI**: Houses numbered 1-6 for each player
- **Internal**: Houses indexed 0-11 in the board array
- **Web UI**: Uses data attributes for proper mapping

## Troubleshooting

### Common Issues

**Web interface not loading:**
- Ensure all files are in the same directory
- Check that port 8000 is not in use
- Verify FastAPI and uvicorn are installed

**AI taking too long:**
- Reduce the depth setting (try 5-7 for good balance)
- Higher depths exponentially increase computation time

**Invalid move errors:**
- Ensure you're clicking on your own houses (bottom row)
- Check that the selected house has beads
- Verify you're following the feeding rule when opponent's side is empty

**Installation issues:**
- Update pip: `pip install --upgrade pip`
- Use virtual environment if needed
- Check Python version compatibility

## Contributing

Feel free to contribute improvements:
- Bug fixes and optimizations
- UI/UX enhancements  
- Additional game variants
- Performance improvements
- Documentation updates

## License

This project is proprietary software. All rights reserved under copyright.
