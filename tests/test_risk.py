cat > tests/test_risk.py <<'PY'
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor

def test_risk_map_shape():
    board = BoardBuilder.from_csv("examples/boards/mini.csv")
    risks = RiskAssessor.estimate(board)
    # every risk key is a (row,col) tuple and there is one entry per cell
    assert len(risks) == board.n_rows * board.n_cols
    assert all(len(key) == 2 for key in risks)
PY
