class ClickEngine:
    """Propagates constraints, reveals safe cells."""
    def __init__(self, board):
        self.board = board

    def reveal_safe_cells(self):
        # TODO: Implement constraint propagation
        pass
    def next_click(self):
        risk_assessor = RiskAssessor(self._board)
        risk_map = risk_assessor.estimate()

        # Filter out revealed cells and get the cell with the lowest probability
        min_prob = float('inf')
        best_cell = None
        for (r, c), prob in risk_map.items():
            if not self._board.grid[r][c].is_revealed and prob < min_prob:
                min_prob = prob
                best_cell = (r, c)

        return best_cell
