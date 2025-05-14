class RiskAssessor:
    """Scores unknown cells for next probe."""
    def __init__(self, board):
        self.board = board

    def score_cells(self):
        # TODO: Implement risk scoring
        pass

    def estimate(self) -> dict:
        risk_map = {}
        for r in range(self._board.n_rows):
            for c in range(self._board.n_cols):
                cell = self._board.grid[r][c]
                if cell.is_flagged:
                    risk_map[(r, c)] = 1.0
                elif cell.is_revealed:
                    risk_map[(r, c)] = 0
                else:
                    risk_map[(r, c)] = 0.15
        return risk_map
