from .risk_assessor import RiskAssessor
from .board import Board


class ClickEngine:
    """Select the next cell to click."""

    @staticmethod
    def next_click(board: Board) -> tuple[int, int]:
        """Return the first still-hidden cell, scanning row-major."""
        for r, row in enumerate(board.grid):
            for c, cell in enumerate(row):
                if cell.state.name == "HIDDEN":
                    return r, c
        return (0, 0)   # all revealed
