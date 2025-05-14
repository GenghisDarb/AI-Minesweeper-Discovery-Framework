from .click_engine import ClickEngine
from .board import Board


class ConstraintSolver:
    """Naive solver: call ClickEngine up to `max_moves` times."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10) -> None:
        for _ in range(max_moves):
            r, c = ClickEngine.next_click(board)
            board.reveal(r, c)
