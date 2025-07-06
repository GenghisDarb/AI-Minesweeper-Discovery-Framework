import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board


def test_board_constructor():
    grid = [["hidden", "mine"], ["hidden", "hidden"]]
    board = Board(grid=grid)
    assert board.n_rows == 2
    assert board.n_cols == 2
    assert board.cells[1].is_mine
