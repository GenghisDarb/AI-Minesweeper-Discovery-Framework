"""
Minesweeper Board implementation with χ‑recursive form and TORUS theory alignment.

This module provides the core Board class with:
- Dynamic mine count tracking for risk tuning
- Safe‑flag handling
- Neighbor references consistent with χ‑recursive model
- Integrated logging for TORUS theory alignment
"""

import json
from datetime import datetime
from typing import List, Optional, Tuple, Iterable
from enum import Enum

from ai_minesweeper.constants import DEBUG
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

from .cell import Cell, State  # re‑export so tests can import State here

__all__ = ["Board", "Cell", "State"]

PathHistory = List[Tuple[int, int]]


class CellState(Enum):
    """Cell states in the minesweeper board."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    SAFE_FLAGGED = "safe_flagged"  # χ‑recursive safe flag


class Board:
    """Core board class implementing χ‑recursive Minesweeper logic."""

    _history: Optional[PathHistory] = None

    def __init__(self, n_rows: Optional[int] = None, n_cols: Optional[int] = None, grid: Optional[Iterable] = None):
        """
        Initialize the board. If `grid` is provided, it should be an iterable of iterables of `Cell` or token values.
        Otherwise, `n_rows` and `n_cols` must be provided and the board will be initialized with hidden cells.
        """
        if grid is None:
            if n_rows is None or n_cols is None:
                raise ValueError("n_rows and n_cols must be provided if grid is None")
            self.grid: List[List[Cell]] = [
                [Cell(row=i, col=j, state=State.HIDDEN) for j in range(n_cols)]
                for i in range(n_rows)
            ]
        else:
            self.grid = []
            for i, row in enumerate(grid):
                cell_row = []
                for j, cell_data in enumerate(row):
                    if isinstance(cell_data, str):
                        token = cell_data.lower()
                        if token == "mine":
                            cell = Cell(row=i, col=j, state=State.HIDDEN, is_mine=True)
                        elif token in (s.value for s in State):
                            cell = Cell(row=i, col=j, state=State(token))
                        else:
                            cell = Cell(row=i, col=j, state=State.HIDDEN)
                    elif isinstance(cell_data, Cell):
                        cell = cell_data
                    else:
                        raise ValueError(f"Invalid cell data: {cell_data}")
                    cell_row.append(cell)
                self.grid.append(cell_row)

        self.n_rows = len(self.grid)
        self.n_cols = len(self.grid[0]) if self.grid else 0

        # Initialize cell coordinates and neighbors
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.row = i
                cell.col = j
                cell.neighbors = self.neighbors(i, j)

        # Board‑level state
        self.custom_neighbors = {}  # Initialize as an empty dictionary
        self.last_safe_reveal: Optional[tuple[int, int]] = None
        self.confidence_history: list[float] = []
        self.chi_cycle_count: int = 0
        self._mines_remaining: int = 0  # optional manual override

        # Debugging: print the initialized grid state
        if DEBUG:
            print("[DEBUG] Board initialized with grid:")
            for row in self.grid:
                print(" ".join(cell.state.name for cell in row))
            print(f"[BOARD INIT] Created Board with {self.n_rows} rows and {self.n_cols} cols")

    # -------------------------------------------------------------------------
    # Construction helpers
    # -------------------------------------------------------------------------
    @staticmethod
    def from_grid(grid: List[List[Cell]]) -> "Board":
        """Construct a Board from a grid of Cell objects."""
        n_rows = len(grid)
        n_cols = len(grid[0]) if n_rows > 0 else 0
        board = Board(n_rows, n_cols)
        board.grid = grid
        return board

    @property
    def cells(self) -> List[Cell]:
        """Flattened list of all cells on the board."""
        return [c for row in self.grid for c in row]

    # -------------------------------------------------------------------------
    # Neighbor handling
    # -------------------------------------------------------------------------
    def neighbors(self, r: int, c: int) -> List[Cell]:
        """Return the list of neighboring Cell objects for the cell at (r, c)."""
        if self.custom_neighbors:
            coords = self.custom_neighbors.get((r, c), [])
            return [self.grid[nr][nc] for (nr, nc) in coords if 0 <= nr < self.n_rows and 0 <= nc < self.n_cols]
        nbrs: List[Cell] = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.n_rows and 0 <= nc < self.n_cols:
                    nbrs.append(self.grid[nr][nc])
        return nbrs

    def adjacent_cells(self, row: int, col: int) -> List[tuple[int, int]]:
        """Return a list of coordinate tuples for all adjacent positions."""
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                    neighbors.append((r, c))
        return neighbors

    # -------------------------------------------------------------------------
    # Basic operations
    # -------------------------------------------------------------------------
    def reveal(self, row: int | tuple[int, int], col: Optional[int] = None, flood: bool = False, visited: Optional[set] = None) -> None:
        """
        Reveal the cell at (row, col) or at the coordinate tuple. If flood is True and the revealed cell has zero adjacent mines,
        recursively reveal all neighbors (standard Minesweeper flood-fill). A visited set is used to avoid infinite recursion.
        """
        if visited is None:
            visited = set()
        if col is None and isinstance(row, tuple):
            row, col = row
        if (row, col) in visited:
            return
        visited.add((row, col))

        cell = self.grid[row][col]
        if cell.state == State.HIDDEN:
            cell.state = State.REVEALED
            self.last_safe_reveal = (row, col)
            if flood and getattr(cell, "adjacent_mines", 0) == 0:
                for neighbor in self.neighbors(row, col):
                    self.reveal((neighbor.row, neighbor.col), flood=True, visited=visited)

    def flag(self, row: int | tuple[int, int], col: Optional[int] = None) -> None:
        """Flag the cell at (row, col) or at the coordinate tuple as a mine."""
        if col is None and isinstance(row, tuple):
            row, col = row
        cell = self.grid[row][col]
        if cell.state == State.HIDDEN:
            cell.state = State.FLAGGED

    # -------------------------------------------------------------------------
    # Utility methods
    # -------------------------------------------------------------------------
    def hidden_cells(self) -> List[Cell]:
        """Return a list of all hidden Cell objects."""
        return [cell for row in self.grid for cell in row if cell.state == State.HIDDEN]

    def revealed_cells(self) -> List[Cell]:
        """Return a list of all revealed Cell objects."""
        return [cell for row in self.grid for cell in row if cell.state == State.REVEALED]

    def print_board(self) -> None:
        """Print the board for debugging purposes."""
        for row in self.grid:
            print("".join(str(cell) for cell in row))

    def clue(self, cell: Cell) -> int:
        """Return the clue number for the given cell (0 if none)."""
        return getattr(cell, "clue", 0) or 0

    # -------------------------------------------------------------------------
    # Validation and state checks
    # -------------------------------------------------------------------------
    def is_valid(self) -> bool:
        """
        Check if the board is in a valid state by verifying that each revealed cell’s clue matches
        the number of adjacent mines.
        """
        for row in self.grid:
            for cell in row:
                if cell.state == State.REVEALED and getattr(cell, "clue", None) is not None:
                    neighbors = self.get_neighbors(cell)
                    mine_count = sum(1 for neighbor in neighbors if neighbor.is_mine)
                    if mine_count != cell.clue:
                        return False
        return True

    def is_solved(self) -> bool:
        """Return True if all non‑mine cells have been revealed."""
        return all(cell.is_mine or cell.state == State.REVEALED for row in self.grid for cell in row)

    def has_unresolved_cells(self) -> bool:
        """Return True if there are any hidden cells remaining on the board."""
        return any(cell.state == State.HIDDEN for row in self.grid for cell in row)

    # -------------------------------------------------------------------------
    # Neighbor utilities used by validation and algorithms
    # -------------------------------------------------------------------------
    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Get neighboring Cell objects for a given cell."""
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = cell.row + dr, cell.col + dc
                if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                    neighbors.append(self.grid[r][c])
        return neighbors

    # -------------------------------------------------------------------------
    # Mines and flagging
    # -------------------------------------------------------------------------
    @property
    def mines_remaining(self) -> int:
        """
        Return the number of mines remaining on the board, computed as the total number of mines
        minus the number of flagged cells. If a manual override has been set via the setter, return that value.
        """
        if hasattr(self, "_mines_remaining") and self._mines_remaining > 0:
            return self._mines_remaining
        total_mines = sum(cell.is_mine for row in self.grid for cell in row)
        flagged_mines = sum(cell.state == State.FLAGGED for row in self.grid for cell in row)
        return total_mines - flagged_mines

    @mines_remaining.setter
    def mines_remaining(self, value: int) -> None:
        if value < 0:
            raise ValueError("Mines remaining cannot be negative.")
        self._mines_remaining = value

    # -------------------------------------------------------------------------
    # Export and representation
    # -------------------------------------------------------------------------
    def export_state(self) -> List[dict]:
        """Export the current board state as a list of dictionaries."""
        return [
            {
                "row": cell.row,
                "col": cell.col,
                "state": cell.state.name,
                "clue": getattr(cell, "clue", 0) or 0,
                "risk": getattr(cell, "risk", None),
            }
            for row in self.grid
            for cell in row
        ]

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        """Allow bracket access (row, col) to the board."""
        r, c = pos
        if not (0 <= r < self.n_rows and 0 <= c < self.n_cols):
            raise IndexError("Board access out of bounds.")
        return self.grid[r][c]

    def __repr__(self) -> str:
        return f"Board(rows={self.n_rows}, cols={self.n_cols})"

    # -------------------------------------------------------------------------
    # Logging for hypothesis testing and χ‑cycle updates
    # -------------------------------------------------------------------------
    def log_state(self, hypothesis_id: str, action: str, confidence: float) -> None:
        """Log the current board state to a .jsonl file with session‑scoped rotation."""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"observer_state_log_{session_id}.jsonl"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "hypothesis_id": hypothesis_id,
            "action": action,
            "confidence": confidence,
            "belief_state": [
                {
                    "row": cell.row,
                    "col": cell.col,
                    "state": cell.state.name,
                    "flagged": cell.state == State.FLAGGED,
                }
                for row in self.grid
                for cell in row
            ],
        }
        with open(log_file, "a") as log:
            log.write(json.dumps(log_entry) + "\n")

    # -------------------------------------------------------------------------
    # Confidence and χ‑cycle integration
    # -------------------------------------------------------------------------
    def calculate_dynamic_threshold(self, mean: float) -> float:
        """Calculate the dynamic confidence threshold based on the mean confidence level."""
        return 0.05 + mean * 0.20

    def update_confidence(self) -> None:
        """Update the board's confidence using the BetaConfidence distribution."""
        confidence = BetaConfidence()
        mean_confidence = confidence.mean()
        self.dynamic_threshold = self.calculate_dynamic_threshold(mean_confidence)
        self.confidence_history.append(mean_confidence)
        self.chi_cycle_count += 1