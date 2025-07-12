from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.board import State

class SpreadRiskAssessor(RiskAssessor):
    """Deterministic stub: spreads probability evenly across all hidden cells."""
    def __init__(self, tau_getter=None):
        """
        Initialize SpreadRiskAssessor with an optional tau getter.
        :param tau_getter: Callable that returns the current tau value.
        """
        self._tau_getter = tau_getter or (lambda: 0.1)  # Default tau value

    def estimate(self, board):
        hidden = [c for row in board.grid for c in row if c.state == State.HIDDEN]
        τ = self._tau_getter()
        base = 1.0 / len(hidden) if hidden else 0.0
        # skew probability: cells with even (row+col) get (base+τ), odd get (base−τ)
        pm = {}
        for c in hidden:
            modifier = τ if (c.row + c.col) % 2 == 0 else -τ
            pm[c] = max(0.0, min(1.0, base + modifier))
        return pm

    def get_probabilities(self, board):
        """
        Return a dictionary of cell probabilities for the given board.
        """
        return self.estimate(board)
