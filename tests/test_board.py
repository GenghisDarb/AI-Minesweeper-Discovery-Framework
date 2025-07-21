import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.board import Board, State


def test_board_constructor():
    grid = [["hidden", "mine"], ["hidden", "hidden"]]
    board = Board(grid=grid)
    assert board.n_rows == 2
    assert board.n_cols == 2
    assert board.grid[0][1].is_mine
    assert board.grid[1][0].state == State.HIDDEN
