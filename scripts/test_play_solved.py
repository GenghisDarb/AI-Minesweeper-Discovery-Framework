import pytest

@pytest.fixture
def csv_path(tmp_path):
    # Provide a default example CSV path for the test
    # You may want to copy a real board file here if needed
    return "examples/boards/sample.csv"
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
    return board.is_solved(), moves

if __name__ == "__main__":
    # Example: run with a small test board
    solved, moves = test_play_and_check_solved("examples/boards/sample.csv")
    print(f"[TEST] Solved: {solved}")
    print(f"[TEST] Move count: {len(moves)}")
