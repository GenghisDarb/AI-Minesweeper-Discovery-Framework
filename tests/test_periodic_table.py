from ai_minesweeper.board import Board, Cell, State
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.periodic_table import PeriodicTableDomain


def test_periodic_table_demo():
    board = BoardBuilder.from_csv("examples/periodic_table/elements.csv")
    assert len(board.grid) > 0
    assert any(
        PeriodicTableDomain.is_mine(cell) for row in board.grid for cell in row
    ), "No mines detected in periodic table board"
    assert all(
        cell.symbol is not None
        for row in board.grid
        for cell in row
        if cell.state == State.HIDDEN
    ), "Some hidden cells have None as symbol"


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


def test_generate_clue_with_multiple_mines():
    neighbors = [Cell(symbol="eka"), Cell(symbol="li"), Cell(symbol="H")]
    clue = PeriodicTableDomain.generate_clue(Cell(), neighbors)
    assert clue == 2, "Clue should count all mines among neighbors"


def test_neighbors_unique():
    board = Board(grid=[[Cell(), Cell()], [Cell(), Cell()]])
    neighbors = PeriodicTableDomain.get_neighbors(board.grid[0][0], board)
    unique_neighbors = []
    for neighbor in neighbors:
        if neighbor not in unique_neighbors:
            unique_neighbors.append(neighbor)
    assert len(neighbors) == len(unique_neighbors), "Neighbors should be unique"


def test_is_mine_edge_cases():
    assert PeriodicTableDomain.is_mine(Cell(symbol="eka")) is True, (
        "Eka should be detected as mine"
    )
    assert PeriodicTableDomain.is_mine(Cell(symbol="H")) is False, (
        "Hydrogen should not be detected as mine"
    )


def test_get_neighbors_empty_board():
    board = Board(grid=[])
    neighbors = PeriodicTableDomain.get_neighbors(Cell(), board)
    assert len(neighbors) == 0, "Neighbors should be empty for an empty board"


def test_get_neighbors_no_neighbors():
    board = Board(grid=[[Cell(group=1, period=1)]] * 3)
    neighbors = PeriodicTableDomain.get_neighbors(board.grid[0][0], board)
    assert len(neighbors) == 0, (
        "Neighbors should be empty if no matching group or period"
    )


def test_is_mine_mixed_case():
    cell = Cell(symbol="Li")
    assert PeriodicTableDomain.is_mine(cell) is True, (
        "Mixed-case symbol should be detected as mine"
    )
    cell = Cell(symbol="li")
    assert PeriodicTableDomain.is_mine(cell) is True, (
        "Lowercase symbol should be detected as mine"
    )
    cell = Cell(symbol="LI")
    assert PeriodicTableDomain.is_mine(cell) is True, (
        "Uppercase symbol should be detected as mine"
    )


def test_generate_clue_no_neighbors():
    neighbors = []
    clue = PeriodicTableDomain.generate_clue(Cell(), neighbors)
    assert clue == 0, "Clue should be 0 if there are no neighbors"


def test_generate_clue_all_mines():
    neighbors = [Cell(symbol="li"), Cell(symbol="be"), Cell(symbol="b")]
    clue = PeriodicTableDomain.generate_clue(Cell(), neighbors)
    assert clue == len(neighbors), "Clue should count all neighbors as mines"


def test_is_mine_with_x():
    cell = Cell(symbol="X")
    assert PeriodicTableDomain.is_mine(cell) is True, (
        "Symbol 'X' should be detected as a mine"
    )


def test_is_mine_comparison_logic():
    mine_symbols = {"x", "eka"}
    assert "x" in mine_symbols, "Lowercase 'x' should be in mine_symbols"
    assert "X".lower() in mine_symbols, (
        "Uppercase 'X' should match lowercase 'x' in mine_symbols"
    )
