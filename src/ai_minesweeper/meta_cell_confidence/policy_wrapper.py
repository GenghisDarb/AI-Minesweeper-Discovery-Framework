from .confidence import BetaConfidence
from ai_minesweeper.board import Board
from ai_minesweeper.cell import Cell
from typing import Any


class ConfidencePolicy:
    """
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(self, base_solver: Any, alpha: float = 1.0, beta: float = 1.0):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param alpha: initial α for confidence prior.
        :param beta: initial β for confidence prior.
        """
        self.solver = base_solver
        self.confidence = BetaConfidence(alpha, beta)
        # Risk threshold τ will be computed each move as a function of confidence

    def choose_move(self, board_state: Board) -> Cell:
        """
        Select the next move based on confidence-adjusted risk threshold.

        :param board_state: Current state of the Minesweeper board.
        :return: The chosen Cell object.
        """
        # 1. Get the probability map from the underlying solver
        prob_map = self.solver.predict(board_state)  # assume returns a 2D array or dict of probabilities for each cell
        hidden_cells = [(r, c) for r, c in prob_map.keys() if board_state.is_hidden(r, c)]

        # 2. Compute dynamic risk threshold τ based on current confidence level
        conf_mean = self.confidence.mean()
        tau = 0.25 - 0.20 * conf_mean   # map confidence to [0.25 (low conf) .. 0.05 (high conf)]

        # 3. Find candidate moves with probability <= τ
        safe_candidates = [cell for cell in hidden_cells if prob_map[cell] <= tau]
        if safe_candidates:
            # choose the candidate with the lowest mine probability
            move = min(safe_candidates, key=lambda cell: prob_map[cell])
        else:
            # no cell is below threshold; take the least risky cell available
            move = min(hidden_cells, key=lambda cell: prob_map[cell])

        # Ensure the returned object is a valid Cell with proper attributes
        r, c = move
        cell = board_state.grid[r][c]
        cell.row, cell.col = r, c

        # 4. Return a Cell object for the chosen move
        if safe_candidates:
            return min(safe_candidates, key=lambda cell: (prob_map[cell], cell.row, cell.col))

        # Fallback: choose the least risky cell
        return min(prob_map.keys(), key=lambda cell: prob_map[cell])
