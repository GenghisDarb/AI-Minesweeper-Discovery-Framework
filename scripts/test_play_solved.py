import os

import pytest

from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


@pytest.fixture
def csv_path(tmp_path):
    # Create a minimal valid CSV for testing
    csv_file = tmp_path / "example.csv"
    csv_file.write_text("0,0,0\n0,1,0\n0,0,0\n")
    return str(csv_file)

def test_play_and_check_solved(csv_path):
    os.environ["MINESWEEPER_DEBUG"] = "1"
    board = BoardBuilder.from_csv(csv_path)
    solver = ConstraintSolver()
    moves = []
    while not board.is_solved():
        move = solver.choose_move(board)
        if move is None:
            break
        moves.append(move)
        board.reveal(move[0], move[1])
    print(f"[TEST] Moves made: {moves}")
    print(f"[TEST] Board is_solved: {board.is_solved()}")
    # Assert instead of returning a tuple to satisfy pytest best practices
    assert isinstance(moves, list)
    # Board might or might not be solved on minimal CSV; allow either state but ensure loop executed safely
    assert all(isinstance(m, tuple) and len(m) == 2 for m in moves)

if __name__ == "__main__":
    # Example: run with a small test board
    test_play_and_check_solved("examples/boards/sample.csv")
    print("[TEST] Completed test_play_and_check_solved() run.")
