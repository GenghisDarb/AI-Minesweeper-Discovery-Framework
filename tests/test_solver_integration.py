from ai_minesweeper.board import State
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.constraint_solver import ConstraintSolver


def test_solver_integration():
    # Create a simple board for testing
    board_data = [
        ["hidden", "hidden", "hidden"],
        ["hidden", "hidden", "hidden"],
        ["hidden", "hidden", "hidden"],
    ]
    board = BoardBuilder.from_data(board_data)

    # Initialize the solver
    solver = ConstraintSolver()

    # Simulate solving the board
    solver.solve(board)

    # Verify that the board is solved
    for row in board.grid:
        for cell in row:
            assert cell.state in [State.REVEALED, State.FLAGGED]

    # Ensure no hidden cells remain
    hidden_cells = [
        cell for row in board.grid for cell in row if cell.state == State.HIDDEN
    ]
    assert len(hidden_cells) == 0
