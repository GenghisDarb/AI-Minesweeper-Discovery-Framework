from .risk_assessor import RiskAssessor
from .board import Board


class ClickEngine:
    """Select the next cell to click."""

    @staticmethod
    def next_click(board: Board) -> tuple[int, int]:
        """Return the unrevealed cell with lowest estimated risk (placeholder)."""
        risks = RiskAssessor.estimate(board)
        return min(risks, key=risks.get, default=(0, 0))
