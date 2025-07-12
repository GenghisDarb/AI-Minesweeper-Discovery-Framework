from .confidence import BetaConfidence
from ai_minesweeper.board import Board, State


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
        :return: The chosen Cell object.
        """
        tau = self.confidence.get_threshold()
        prob_map = self.base_solver.estimate(board_state)
        if not prob_map:
            prob_map = {
                cell: 0.5
                for row in board_state.grid
                for cell in row
                if cell.state == State.HIDDEN
            }
        # Λ-ladder curve (Observer-State §2.3):
        # early confidence moves the threshold quickly; high confidence tapers.
        tau_min, tau_max = 0.05, 0.25
        tau = tau_min + (tau_max - tau_min) * (1 - self.confidence.mean()) ** 2

        print(f"Using Λ-ladder threshold: {tau}")

        safe_cells = [cell for cell, prob in prob_map.items() if prob <= tau]
        return min(safe_cells, key=lambda cell: (prob_map[cell], cell.row, cell.col)) if safe_cells else None
