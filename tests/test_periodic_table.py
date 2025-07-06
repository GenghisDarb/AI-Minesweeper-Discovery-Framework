import pytest
from ai_minesweeper.domain.periodic_table import PeriodicTableDomain
from ai_minesweeper.board_builder import BoardBuilder

def test_periodic_table_demo():
    board = BoardBuilder.from_csv("examples/periodic_table/elements.csv")
    assert len(board.cells) > 0
    assert any(cell.is_mine for cell in board.cells)
    assert all(len(cell.neighbors) > 0 for cell in board.cells)
