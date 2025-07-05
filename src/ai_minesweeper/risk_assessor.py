from .board import Board, State

class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[tuple[int, int], float]:
        risk_map: dict[tuple[int, int], float] = {}
        for r, row in enumerate(board.grid):
            for c, cell in enumerate(row):
                if cell.state == State.HIDDEN:
                    risk_map[(r, c)] = 0.15  # placeholder uniform risk
                elif cell.is_mine:
                    risk_map[(r, c)] = 1.0
                else:
                    risk_map[(r, c)] = 0.0
        return risk_map

    @staticmethod
    def pick_cell(board: Board) -> tuple[int, int]:
        """
        Select the next cell to probe based on risk assessment.
        """
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.state == State.HIDDEN:
                    return r, c
        return None, None
