import logging
import os

from .board import Board, State  # Import State to resolve NameError
from .meta_cell_confidence.confidence import BetaConfidence
from .meta_cell_confidence.policy_wrapper import ConfidencePolicy
from .risk_assessor import RiskAssessor
from .solver_logic import CascadePropagator, Flagger


class ConstraintSolver:
    """Naive solver: call ClickEngine up to `max_moves` times."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10) -> None:
        """Run a small, safe solve loop that always makes forward progress or exits.

        Caps steps and bails on no-progress to avoid stalls in tests.
        """
        # Initialize confidence module
        confidence = BetaConfidence()
        policy = ConfidencePolicy(RiskAssessor(), confidence)
        MAX_STEPS_ENV = int(os.getenv("MINESWEEPER_MAX_STEPS", str(max_moves)))
        NO_PROGRESS_LIMIT = 10
        cap = min(max_moves, MAX_STEPS_ENV) if max_moves is not None else MAX_STEPS_ENV

        def revealed_count() -> int:
            return sum(
                1
                for row in board.grid
                for cell in row
                if getattr(cell, "state", None) is not None and getattr(cell.state, "name", None) == "REVEALED"
            )

        moves = 0
        no_progress = 0
        last_revealed = revealed_count()

        while moves < cap:
            # Simple deduction pass (safe and contradictions)
            deduction_made = True
            while deduction_made:
                deduction_made = Flagger.mark_contradictions(board) or CascadePropagator.open_safe_neighbors(board)

            # If everything relevant is revealed, stop
            if all(cell.state != State.HIDDEN for row in board.grid for cell in row if not getattr(cell, "is_false_hypothesis", False)):
                logging.info("All valid hypotheses resolved. Discovery complete!")
                logging.debug(f"Final board state: {board}")
                return

            # Ask policy for next move
            move = policy.choose_move(board)
            if move is None:
                logging.info("No moves left to make.")
                logging.debug(f"Board state when no moves left: {board}")
                return

            # Normalize move to coordinates
            if hasattr(move, "row") and hasattr(move, "col"):
                r, c = int(move.row), int(move.col)
            elif isinstance(move, tuple) and len(move) == 2:
                r, c = int(move[0]), int(move[1])
            else:
                logging.debug(f"Unsupported move type {type(move)}; aborting move.")
                return

            # Skip illegal/duplicate moves and count as no progress
            if hasattr(board, "is_hidden") and not board.is_hidden((r, c)):
                no_progress += 1
            else:
                # Reveal, counting progress only on actual state change
                try:
                    changed = bool(getattr(board, "reveal_cell", getattr(board, "reveal"))(r, c))
                except Exception:
                    changed = False
                now_revealed = revealed_count()
                if not changed and now_revealed == last_revealed:
                    no_progress += 1
                else:
                    no_progress = 0
                    last_revealed = now_revealed
                moves += 1

            # Bail if we can't make progress deterministically
            if no_progress >= NO_PROGRESS_LIMIT:
                logging.info("No progress after consecutive attempts; exiting to avoid stall.")
                return
