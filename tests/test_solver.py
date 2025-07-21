from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import ConstraintSolver


def test_solver_runs():
    board = BoardBuilder.from_csv("examples/boards/mini.csv")
    ConstraintSolver.solve(board, max_moves=3)
    # at least one cell should now be non-hidden
    assert any(cell.state.name != "HIDDEN" for row in board.grid for cell in row)
