from ai_minesweeper.board import Board               # ← added import
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.click_engine import ClickEngine


def test_lowest_risk_chosen():
    """The cell chosen by ClickEngine must not be a mine on mini.csv."""
    board: Board = BoardBuilder.from_csv("examples/boards/mini.csv")
    r, c = ClickEngine.next_click(board)
    assert not board.grid[r][c].is_mine, "ClickEngine chose a mined cell!"


def test_risk_zero_with_zero_adjacent():
    """After revealing a 0-adjacent cell, all hidden neighbours should have risk 0."""
    # Build an empty 3×3 board with no mines
    board = Board(3, 3)
    for row in board.grid:
        for cell in row:
            cell.adjacent_mines = 0

    board.reveal(1, 1)  # reveal the center cell (adjacent count = 0)
    risks = RiskAssessor.estimate(board)

    # Every hidden cell should now have risk 0.0
    assert all(val == 0.0 for key, val in risks.items() if key != (1, 1))
