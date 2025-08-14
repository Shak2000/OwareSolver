from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

app = FastAPI()
game = Game()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start():
    game.start()


@app.post("/switch")
async def switch():
    game.switch()


@app.get("/get_winner")
async def get_winner():
    return game.get_winner()


@app.post("/undo")
async def undo():
    return game.undo()


@app.get("/simulate_move")
async def simulate_move(house, board, top_score, bottom_score, player):
    return game.simulate_move(house, board, top_score, bottom_score, player)


@app.post("/move")
async def move(house):
    return game.move(house)


@app.get("/get_possible_moves")
async def get_possible_moves(board, player):
    return game.get_possible_moves(board, player)


@app.get("/evaluate_board")
async def evaluate_board(board, top_score, bottom_score):
    return game.evaluate_board(board, top_score, bottom_score)


@app.get("/minimax")
async def minimax(board, top_score, bottom_score, player, depth, alpha, beta):
    return game.minimax(board, top_score, bottom_score, player, depth, alpha, beta)


@app.post("/ai_move")
async def ai_move(depth):
    return game.ai_move(depth)
