from .risk_assessor import RiskAssessor
from .board import Board


class ClickEngine:
    """Select the next cell to click."""

    @staticmethod
    def     @staticmethod
    def next_click(board: Board) -> tuple[int, int]:
        """Return the hidden cell with the lowest estimated risk."""
        risks = RiskAssessor.estimate(board)
        # Filter for hidden cells
        hidden_cells = {(r, c): risk for (r, c), risk in risks.items() if board.grid[r][c].state == State.HIDDEN}
        # Return the hidden cell with the lowest risk, prioritizing lowest row and column in case of ties
        return min(hidden_cells, key=lambda cell: (hidden_cells[cell], cell))        return min(risks, key=risks.get, default=(0, 0))
