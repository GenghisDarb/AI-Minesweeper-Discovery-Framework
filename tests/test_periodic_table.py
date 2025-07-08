from ai_minesweeper.board import Board, Cell
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.domain.periodic_table import PeriodicTableDomain


def test_periodic_table_demo():
    board = BoardBuilder.from_csv("examples/periodic_table/elements.csv")
    assert len(board.grid) > 0
    assert any(cell.is_mine for row in board.grid for cell in row), (
        "No mines detected in periodic table board"
    )


def test_get_neighbors():
    board = Board(grid=[[Cell(), Cell()], [Cell(), Cell()]])
    neighbors = PeriodicTableDomain.get_neighbors(board.grid[0][0], board)
    assert len(neighbors) == 3


def test_is_mine():
    cell = Cell(symbol="eka")
    assert PeriodicTableDomain.is_mine(cell) is True
    cell = Cell(symbol="H")
    assert PeriodicTableDomain.is_mine(cell) is False


def test_generate_clue():
    neighbors = [Cell(symbol="eka"), Cell(symbol="H")]
    clue = PeriodicTableDomain.generate_clue(Cell(), neighbors)
    assert clue == 1
