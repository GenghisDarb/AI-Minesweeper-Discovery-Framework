import pytest
from ai_minesweeper.domain_loader import DomainLoader
from ai_minesweeper.cell import State


def test_nuclear_adapter():
    board = DomainLoader.load("periodic-table-v2")
    assert len(board.cells) >= 3000

    moves = 0
    for _ in range(20):
        move = board.solve_next()
        if move is None:
            break
        moves += 1

    flagged_cells = [
        cell for cell in board.cells if cell.is_mine and cell.state == State.FLAGGED
    ]
    assert len(flagged_cells) > 0
