from typing import Generator, Optional, Tuple

from ai_minesweeper.cell import Cell
from ai_minesweeper.constants import DEBUG

from .board import Board, State


class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[Cell, float]:
        """
        Return a rank-ordered false-hypothesis-probability map.

        :param board: The current board state.
        :return: A dictionary mapping Cell objects to probabilities.
        """
        if DEBUG:
            print("[DEBUG] Board state in RiskAssessor.estimate:")
            for row in board.grid:
                print(" ".join(cell.state.name for cell in row))

        hidden_cells = board.hidden_cells()
        if DEBUG:
            print(f"[RiskAssessor] Hidden cells found: {len(hidden_cells)}")

        base_p = board.false_hypotheses_remaining / len(hidden_cells)
        last_safe = board.last_safe_reveal or (board.n_rows // 2, board.n_cols // 2)

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        probs: dict[Cell, float] = {}
        for cell in hidden_cells:
            adj = board.adjacent_cells(cell.row, cell.col)
            flagged = sum(1 for v in adj if board.is_flagged(v))
            hidden_adj = sum(1 for v in adj if board.is_hidden(v))

            local_risk = (flagged / hidden_adj) if hidden_adj else 0
            dist_risk = manhattan((cell.row, cell.col), last_safe) / (
                board.n_rows + board.n_cols
            )

            prob = min(
                0.95,
                base_p + 1.0 * local_risk + 0.8 * dist_risk,
            )
            probs[cell] = prob

        return probs

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

    def handle_contradiction(self, board, cell):
        """
        Handle a contradiction (mine) without ending the session.

        Args:
            board (Board): The current game board.
            cell (Cell): The cell that caused the contradiction.
        """
        cell.state = State.FLAGGED
        board.update_confidence()  # Update confidence after marking the contradiction
        print(
            f"[INFO] Contradiction at {cell.row}, {cell.col} flagged. Confidence updated."
        )

    @staticmethod
    def choose_move(board: Board) -> Cell:
        """
        Select the cell with the lowest risk.

        :param board: The current board state.
        :return: The chosen Cell object.
        """
        prob_map = RiskAssessor.estimate(board)
        return min(prob_map, key=prob_map.get)

    def iter_safe_candidates(
        self, board: "Board"
    ) -> Generator[Cell, None, None]:
        """
        Yield safe candidate cells based on risk assessment.

        :param board: The current board state.
        :yield: Safe Cell objects.
        """
        prob_map = RiskAssessor.estimate(board)
        for cell, prob in prob_map.items():
            if prob < 0.25:
                yield cell


class SpreadRiskAssessor(RiskAssessor):
    def __init__(self, tau_getter=lambda: 0.1):
        """Initialize the SpreadRiskAssessor with an optional tau_getter."""
        self.tau_getter = tau_getter

    def estimate(self, board):
        """Estimate probabilities for all hidden cells on the board."""
        return self.get_probabilities(board)

    def get_probabilities(self, board):
        """Spread equal probability across all hidden cells with slight variation."""
        hidden_cells = [
            (cell.row, cell.col)
            for row in board.grid
            for cell in row
            if cell.is_hidden()
        ]
        num_hidden = len(hidden_cells)
        if num_hidden == 0:
            return {}

        base_prob = 1 / num_hidden
        tau = self.tau_getter()
        probabilities = {}

        for idx, (row, col) in enumerate(hidden_cells):
            variation = tau if idx % 2 == 0 else -tau
            probabilities[(row, col)] = max(0, base_prob + variation)

        return probabilities

    def predict(self, board):
        """Predict probabilities for all cells on the board."""
        return self.get_probabilities(board)

    def normalize(self, risk_map: dict[Cell, float]) -> dict[Cell, float]:
        """Normalize the risk map to sum to one."""
        total = sum(risk_map.values())
        return {cell: risk / total for cell, risk in risk_map.items()}
