from __future__ import annotations

from typing import Dict, Tuple

from ai_minesweeper.board import Board, State  # adjust path if your package layout differs


def compute_probabilities(board: Board) -> Dict[Tuple[int, int], float]:
    """Return a mapping (row, col) → probability that the cell is a mine.

    Currently assigns a uniform 0.15 probability to every hidden cell,
    1.0 to known mines, and 0.0 to revealed safe cells.  Replace the
    placeholder logic with a real solver when you’re ready.
    """
    risk_map: Dict[Tuple[int, int], float] = {}

    for r, row in enumerate(board.grid):
        for c, cell in enumerate(row):
            if cell.state == State.HIDDEN:
                # TODO: replace with actual probability calculation
                risk_map[(r, c)] = 0.15
            elif cell.is_mine:
                risk_map[(r, c)] = 1.0
            else:
                risk_map[(r, c)] = 0.0

    return risk_map


def choose_move(board: Board) -> Tuple[int, int]:
    """Return the hidden cell with the lowest mine probability."""
    probs = compute_probabilities(board)
    # Safest move = min-probability hidden cell
    return min(probs.items(), key=lambda item: item[1])[0]

