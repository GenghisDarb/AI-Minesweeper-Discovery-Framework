from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor


def test_risk_map_shape():
    board = BoardBuilder.from_csv("examples/boards/mini.csv")
    risks = RiskAssessor.estimate(board)
    # one risk entry per cell and each key is (row, col)
    assert len(risks) == board.n_rows * board.n_cols
    assert all(len(key) == 2 for key in risks)

def test_single_clue_probabilities():
    board = BoardBuilder.from_ascii(
        "1.\n.."
    ).build()
    ass = RiskAssessor(board)
    probs = ass.estimate()
    # only (1,1) must be 0, the mine is either (0,1) or (1,0): 50/50
    assert probs[(0,1)] == pytest.approx(0.5, abs=1e-6)
    assert probs[(1,0)] == pytest.approx(0.5, abs=1e-6)
