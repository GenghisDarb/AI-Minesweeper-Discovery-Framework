from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.board_builder import BoardBuilder

def test_choose_move_returns_valid_hidden_cell():
    board = BoardBuilder.from_csv("tests/data/test_grid.csv")
    move = RiskAssessor().choose_move(board)
    assert move is not None
    # move should be a Cell object with row/col attributes
    assert hasattr(move, 'row') and hasattr(move, 'col')
    r, c = move.row, move.col
    cell = board.grid[r][c]
    assert cell.is_hidden()
