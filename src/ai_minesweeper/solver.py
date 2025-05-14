from .click_engine import ClickEngine
from .board import Board


class ConstraintSolver:
    """Naive solver loop."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10):
        for _ in range(max_moves):
            r, c = ClickEngine.next_click(board)
            board.reveal(r, c)
