import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board
from ai_minesweeper.solver_logic import SolverLogic


def test_solver_basic():
    board = Board(
        [
            ["hidden", "hidden", "hidden"],
            ["hidden", "mine", "hidden"],
            ["hidden", "hidden", "hidden"],
        ]
    )
    SolverLogic.flag_mines(board)
    SolverLogic.cascade_reveal(board)
    assert all(
        cell.state == "revealed"
        for row in board.cells
        for cell in row
        if not cell.is_mine
    )
