import logging

from .board import Board, State  # Import State to resolve NameError
from .meta_cell_confidence.confidence import BetaConfidence
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
from .risk_assessor import RiskAssessor
from .solver_logic import CascadePropagator, Flagger


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
                if not cell.is_false_hypothesis
            ):
                logging.info("All valid hypotheses resolved. Discovery complete!")
                logging.debug(f"Final board state: {board}")
                return

            move = policy.choose_move(board)
            row, col = move  # Unpack tuple
            if move is None:
                logging.info("No moves left to make.")
                logging.debug(f"Board state when no moves left: {board}")
                return

            logging.debug(f"Testing hypothesis at ({move.row}, {move.col})")
            logging.debug(f"Current board state: {board}")
