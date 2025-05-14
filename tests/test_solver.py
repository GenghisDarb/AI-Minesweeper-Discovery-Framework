cat > tests/test_solver.py <<'PY'
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import ConstraintSolver

def test_solver_runs():
    board = BoardBuilder.from_csv("examples/boards/mini.csv")
    # Should run without raising and reveal at least one cell
    ConstraintSolver.solve(board, max_moves=3)
    assert any(cell.state.name != "HIDDEN" for row in board.grid for cell in row)
PY
