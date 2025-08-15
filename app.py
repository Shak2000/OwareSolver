from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

app = FastAPI()
game = Game()


# Pydantic model for game state, useful for type hinting and documentation
class GameState(BaseModel):
    board: list[int]
    top: int
    bottom: int
    player: str
    history_length: int
    winner: str | None


@app.get("/")
async def get_ui():
    """Returns the main HTML file for the UI."""
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    """Returns the CSS stylesheet."""
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    """Returns the JavaScript file for the UI logic."""
    return FileResponse("script.js")


@app.get("/get_game_state", response_model=GameState)
async def get_game_state():
    """Returns the entire current game state."""
    return GameState(
        board=game.board,
        top=game.top,
        bottom=game.bottom,
        player=game.player,
        history_length=len(game.history),
        winner=game.get_winner()
    )


@app.post("/start")
async def start():
    """Starts a new game."""
    game.start()


@app.post("/switch")
async def switch():
    """Switches the current player."""
    game.switch()


@app.post("/undo")
async def undo():
    """Undoes the last move."""
    game.undo()


@app.post("/move/{house}")
async def move(house: int):
    """Makes a move for the current player."""
    return game.move(house)


@app.post("/ai_move/{depth}")
async def ai_move(depth: int):
    """Triggers an AI move with the specified depth."""
    return game.ai_move(depth)
