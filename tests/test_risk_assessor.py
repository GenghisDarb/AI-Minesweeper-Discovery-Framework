from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.board_builder import BoardBuilder


def test_choose_move_returns_valid_hidden_cell():
    board = BoardBuilder.from_csv("tests/data/test_grid.csv")
    move = RiskAssessor().choose_move(board)
    assert move is not None
    r, c = move
    cell = board.grid[r][c]
    assert cell.is_hidden()
