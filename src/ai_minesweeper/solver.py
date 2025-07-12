from .board import Board, State  # Import State to resolve NameError
from .solver_logic import Flagger, CascadePropagator
from .risk_assessor import RiskAssessor
from .meta_cell_confidence.confidence import BetaConfidence
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
import logging


class ConstraintSolver:
    """Naive solver: call ClickEngine up to `max_moves` times."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10) -> None:
        # Initialize confidence module
        confidence = BetaConfidence()
        policy = ConfidencePolicy(base_solver=RiskAssessor, confidence=confidence)

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
                logging.info("All safe cells revealed. Discovery complete!")
                return

            move = policy.choose_move(board)
            if move is None:
                logging.info("No moves left to make.")
                return

            logging.debug(f"Revealing cell at ({move.row}, {move.col})")
            board.reveal(move.row, move.col, flood=True)
            moves += 1
