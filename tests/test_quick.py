import pytest
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor

# Path to your periodic table hypothesis grid
CSV_PATH = "examples/periodic_table/elements.csv"

def test_risk_assessor_estimate_structure():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    prob_map = assessor.estimate(board)

    assert isinstance(prob_map, dict)
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in prob_map)
    assert all(isinstance(p, float) for p in prob_map.values())

def test_risk_assessor_estimate_behavior():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    prob_map = assessor.estimate(board)

    hidden_cells = [(r, c) for (r, c) in prob_map if board[r, c].is_hidden()]
    assert len(hidden_cells) > 0, "Expected some hidden cells in the estimate result"

def test_risk_assessor_choose_move_returns_hidden():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    move = assessor.choose_move(board)

    assert move is not None
    r, c = move
    assert board[r, c].is_hidden(), f"Cell {r,c} was not hidden when selected"
