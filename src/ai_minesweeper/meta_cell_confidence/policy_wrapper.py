from ai_minesweeper.board import Board
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


class ConfidencePolicy:
    """
    Confidence-aware move selection policy.
    Adjusts risk tolerance dynamically based on solver confidence.
    """

    def __init__(self, base_solver, confidence: BetaConfidence):
        """
        Initialize with a base solver and confidence tracker.
        :param base_solver: Solver providing mine probability estimates.
        :param confidence: BetaConfidence instance for tracking.
        """
        self.base_solver = base_solver()
        self.confidence = confidence

    def choose_move(self, board_state: Board):
        """
        Select the next move based on confidence-adjusted risk threshold.
        :param board_state: Current state of the Minesweeper board.
        :return: Coordinates of the chosen cell (row, col).
        """
        prob_map = self.base_solver.estimate(board_state)
        if not prob_map:
            prob_map = {
                (cell.row, cell.col): 0.5
                for row in board_state.grid
                for cell in row
                if cell.state == State.HIDDEN
            }
        tau = 0.05 + self.confidence.mean() * (0.25 - 0.05)

        # Find safe cells under the threshold
        safe_cells = [(r, c) for (r, c), p in prob_map.items() if p <= tau]
        if safe_cells:
            chosen_cell = min(safe_cells, key=lambda cell: prob_map[cell])
        elif prob_map:
            # Forced exploration: pick the least risky cell
            chosen_cell = min(prob_map.keys(), key=lambda cell: prob_map[cell])
        else:
            # Guaranteed-safe fallback: scan row-major order for first legal move
            # Debug fallback logic: ensure valid move is identified
            for r in range(board_state.n_rows):
                for c in range(board_state.n_cols):
                    cell = board_state.grid[r][c]
                    print(
                        f"Checking cell at ({r}, {c}): state={cell.state}, is_mine={cell.is_mine}, flagged={cell.state == State.FLAGGED}"
                    )
                    if (
                        cell.state == State.HIDDEN
                        and not cell.is_mine
                        and cell.state != State.FLAGGED
                    ):
                        return r, c

            raise RuntimeError("No valid moves remaining on the board.")

        return chosen_cell
