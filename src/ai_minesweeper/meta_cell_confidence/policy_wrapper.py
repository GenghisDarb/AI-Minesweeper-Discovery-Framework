from typing import Any

from ai_minesweeper.board import Board
from ai_minesweeper.cell import Cell

from .confidence import BetaConfidence


class ConfidencePolicy:
    """
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(
        self,
        base_solver: Any,
        alpha: float = 1.0,
        beta: float = 1.0,
        confidence: BetaConfidence | None = None,
    ):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param alpha: initial α for confidence prior.
        :param beta: initial β for confidence prior.
        :param confidence: Optional pre-initialized confidence tracker.
        """
        self.solver = base_solver
        self.confidence = confidence if confidence else BetaConfidence(alpha, beta)
        # Risk threshold τ will be computed each move as a function of confidence

    def choose_move(self, board_state: Board) -> Cell:
        """
        Select the next move based on confidence-adjusted risk threshold.

        :param board_state: Current state of the Minesweeper board.
        :return: The chosen Cell object.
        """
        # 1. Get the probability map from the underlying solver
        prob_map = self.solver.estimate(board_state)  # Use RiskAssessor's estimate method

        hidden_cells = [
            cell for row in board_state.grid for cell in row if board_state.is_hidden(cell)
        ]

        # 2. Compute dynamic risk threshold τ based on current confidence level
        tau = self.confidence.get_threshold()

        # 3. Find candidate moves with probability <= τ
        safe_candidates = [cell for cell in hidden_cells if prob_map[cell] <= tau]
        if safe_candidates:
            # choose the candidate with the lowest mine probability
            move = min(safe_candidates, key=lambda cell: prob_map[cell])
        else:
            # no cell is below threshold; take the least risky cell available
            move = min(hidden_cells, key=lambda cell: prob_map[cell])

        return move
