from ai_minesweeper.board import Board, State
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


class ConfidencePolicy:
    """
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(self, base_solver, confidence: BetaConfidence):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param confidence: BetaConfidence instance for tracking.
        """
        self.base_solver = base_solver()
        self.confidence = confidence

    def choose_move(self, board_state: Board):
        """
        Select the next move based on confidence-adjusted risk threshold.
        :param board_state: Current state of the Minesweeper board.
        :return: Coordinates of the chosen cell (row, col).
        """
        prob_map = self.base_solver.estimate(board_state)
        if not prob_map:
            prob_map = {
                (cell.row, cell.col): 0.5
                for row in board_state.grid
                for cell in row
                if cell.state == State.HIDDEN
            }
        # Λ-ladder curve (Observer-State §2.3):
        # early confidence moves the threshold quickly; high confidence tapers.
        tau_min, tau_max = 0.05, 0.25
        tau = tau_min + (tau_max - tau_min) * (1 - self.confidence.mean()) ** 2

        print(f"Using Λ-ladder threshold: {tau}")

        # Find safe cells under the threshold
        safe_cells = [(r, c) for (r, c), p in prob_map.items() if p <= tau]
        print(f"Filtered safe cells: {safe_cells}")
        if safe_cells:
            chosen_cell = min(safe_cells, key=lambda cell: prob_map[cell])
        elif prob_map:
            # Forced exploration: pick the least risky cell
            chosen_cell = min(prob_map.keys(), key=lambda cell: prob_map[cell])
        else:
            # Guaranteed-safe fallback: scan row-major order for first legal move
            # Debug fallback logic: ensure valid move is identified
            for r in range(board_state.n_rows):
                for c in range(board_state.n_cols):
                    cell = board_state.grid[r][c]
                    print(
                        f"Checking cell at ({r}, {c}): state={cell.state}, is_mine={cell.is_mine}, flagged={cell.state == State.FLAGGED}"
                    )
                    if (
                        cell.state == State.HIDDEN
                        and not cell.is_mine
                        and cell.state != State.FLAGGED
                    ):
                        return r, c

            raise RuntimeError("No valid moves remaining on the board.")

        # Adjust probability map based on threshold
        prob_map = {
            coords: p * (1 - tau) if tau < 0.5 else p * tau
            for coords, p in prob_map.items()
        }

        # Re-filter safe cells after adjustment
        safe_cells = [(r, c) for (r, c), p in prob_map.items() if p <= tau]
        print(f"Re-filtered safe cells: {safe_cells}")

        # Select move based on adjusted probabilities
        if tau < 0.5:
            # Low confidence: prioritize exploration
            chosen_cell = min(safe_cells, key=lambda cell: prob_map[cell]) if safe_cells else min(prob_map.keys(), key=lambda cell: prob_map[cell])
        else:
            # High confidence: prioritize safety
            chosen_cell = max(safe_cells, key=lambda cell: prob_map[cell]) if safe_cells else max(prob_map.keys(), key=lambda cell: prob_map[cell])

        return chosen_cell


from typing import Any
from .confidence import BetaConfidence


class ConfidencePolicy:
    """
    Wraps a solver with a confidence-based policy for move selection.

    Attributes:
        solver (Any): The original solver instance.
        confidence_tracker (BetaConfidence): Tracks confidence in predictions.
    """

    def __init__(self, solver: Any):
        self.solver = solver
        self.confidence_tracker = BetaConfidence()

    def choose_move(self, board: Any) -> Any:
        """
        Chooses the next move based on confidence and risk threshold.

        Args:
            board (Any): The current game board state.

        Returns:
            Any: The chosen move.
        """
        probability_map = self.solver.get_probability_map(board)
        confidence = self.confidence_tracker.mean()
        risk_threshold = 0.05 + 0.2 * confidence

        for cell, prob in probability_map.items():
            if prob < risk_threshold:
                return cell

        # Default to the most informative hidden cell
        return max(probability_map, key=probability_map.get)
