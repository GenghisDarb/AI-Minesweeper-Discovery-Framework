from .click_engine import ClickEngine
from .board import Board, State  # Import State to resolve NameError
from .solver_logic import Flagger, CascadePropagator
from .risk_assessor import RiskAssessor


class ConstraintSolver:
    """Naive solver: call ClickEngine up to `max_moves` times."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10) -> None:
        moves = 0
        while moves < max_moves:
            deduction_made = True
            while deduction_made:
                deduction_made = Flagger.mark_contradictions(
                    board
                ) or CascadePropagator.open_safe_neighbors(board)

            if all(
                cell.state != State.HIDDEN
                for row in board.grid
                for cell in row
                if not cell.is_mine
            ):
                print("All safe cells revealed. Discovery complete!")
                return

            r, c = RiskAssessor.pick_cell(board)
            if r is None or c is None:
                print("No moves left to make.")
                return

            board.reveal(r, c, flood=True)
            moves += 1
