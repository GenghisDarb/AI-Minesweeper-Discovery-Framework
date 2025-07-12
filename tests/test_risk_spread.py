from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.board_builder import BoardBuilder


def test_risk_has_variance():
    board = BoardBuilder.random_board(rows=4, cols=4, mines=2)
    ra = RiskAssessor()
    pm = ra.estimate(board)
    assert len(set(pm.values())) > 1, "probabilities should not be uniform"
