from .board import Board, State

class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
   def compute_probabilities(board: Board) -> dict[tuple[int, int], float]:
    """Return a mapping (row, col) → mine probability."""
    risk_map: dict[tuple[int, int], float] = {}

    for r, row in enumerate(board.grid):
        for c, cell in enumerate(row):
            if cell.state == State.HIDDEN:
                # placeholder uniform risk
                risk_map[(r, c)] = 0.15
            elif cell.is_mine:
                risk_map[(r, c)] = 1.0
            else:
                risk_map[(r, c)] = 0.0

    return risk_map
