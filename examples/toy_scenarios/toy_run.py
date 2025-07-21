import json

from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import ConstraintSolver

# Load toy board
with open("toy_board.json") as f:
    board_data = json.load(f)

board = BoardBuilder.from_json(board_data)

# Run confidence oscillation sweep
ConstraintSolver.solve(board, max_moves=3)

# Output log
with open("toy_run.log", "w") as log_file:
    for state in board.history():
        log_file.write(f"{state}\n")
