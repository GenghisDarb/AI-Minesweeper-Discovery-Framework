"""
Minesweeper Board implementation with χ-recursive form and TORUS theory alignment.

This module provides the core Board class with:
- Dynamic mine count tracking for risk tuning
- Safe-flag handling
- Neighbor references consistent with χ-recursive model
- Integrated logging for TORUS theory alignment
"""

import json
import logging
from datetime import datetime
from typing import List, Optional, Tuple, Set, Dict
from enum import Enum

from ai_minesweeper.constants import DEBUG

from .cell import Cell, State  # re-export so tests can import State here

__all__ = ["Board", "Cell", "State"]  # optional but nice

PathHistory = List[Tuple[int, int]]


class CellState(Enum):
    """Cell states in the minesweeper board."""
    HIDDEN = "hidden"
    REVEALED = "revealed" 
    FLAGGED = "flagged"
    SAFE_FLAGGED = "safe_flagged"  # χ-recursive safe flag


class Board:
    _history: Optional[PathHistory] = None

    def __init__(
        self, n_rows: Optional[int] = None, n_cols: Optional[int] = None, grid=None
    ):
        if DEBUG:
            print(f"[DEBUG] Board.__init__ received grid: type={type(grid)}")
            if isinstance(grid, list):
                print(f"[DEBUG] grid has {len(grid)} rows")
                if len(grid) > 0:
                    print(
                        f"[DEBUG] first row type: {type(grid[0])}, length: {len(grid[0])}"
                    )
                    print(f"[DEBUG] first cell sample: {repr(grid[0][0])}")
                else:
                    print("[DEBUG] grid is an empty list")
            else:
                print("[DEBUG] grid is NOT a list")

        if grid is None:
            if n_rows is None or n_cols is None:
                raise ValueError("n_rows and n_cols must be provided if grid is None")
            self.grid = [
                [Cell(row=i, col=j, state=State.HIDDEN) for j in range(n_cols)]
                for i in range(n_rows)
            ]
        else:
            self.grid = []
            for i, row in enumerate(grid):
                cell_row = []
                for j, cell_data in enumerate(row):
                    if isinstance(cell_data, str):
                        if cell_data.lower() == "mine":
                            cell = Cell(row=i, col=j, state=State.MINE, is_mine=True)
                        elif cell_data in [s.value for s in State]:
                            cell = Cell(row=i, col=j, state=State(cell_data))
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

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.row = i
                cell.col = j
                cell.neighbors = self.adjacent_cells(i, j)

        if self.n_rows < 0 or self.n_cols < 0:
            raise ValueError("Board dimensions must be non-negative integers.")

        for row in self.grid:
            for cell in row:
                if cell.row < 0 or cell.col < 0:
                    raise ValueError("Cell coordinates must be non-negative.")
        self.custom_neighbors: dict[tuple[int, int], list[tuple[int, int]]] | None = (
            None  # Logical neighbor map
        )
        self.last_safe_reveal: tuple[int, int] | None = (
            None  # Track the last safe cell revealed
        )

        for row in self.grid:
            for cell in row:
                cell.neighbors = self.adjacent_cells(cell.row, cell.col)

        self.log_file = "board_state_log.jsonl"
        self.false_hypotheses_remaining: int = (
            0  # Tracks the number of false hypotheses remaining on the board
        )
        self.mines_remaining: int = (
            0  # Tracks the number of mines remaining on the board
        )

        # Debugging: Print the initialized grid state
        if DEBUG:
            print("[DEBUG] Board initialized with grid:")
            for row in self.grid:
                print(" ".join(cell.state.name for cell in row))
            print(
                f"[BOARD INIT] Created Board with {self.n_rows} rows and {self.n_cols} cols"
            )
            print(f"[BOARD INIT] Board id={id(self)}, grid id={id(self.grid)}")

    @staticmethod
    def from_grid(grid):
        """Construct a Board from a grid of Cell objects."""
        n_rows = len(grid)
        n_cols = len(grid[0]) if n_rows > 0 else 0
        board = Board(n_rows, n_cols)
        board.grid = grid
        return board

    @property
    def cells(self) -> list[Cell]:
        return [c for row in self.grid for c in row]

    def neighbors(self, r, c):
        if self.custom_neighbors is not None:
            return [
                self.grid[nr][nc] for (nr, nc) in self.custom_neighbors.get((r, c), [])
            ]
        # Default to physical adjacency
        nbrs = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.n_rows and 0 <= nc < self.n_cols:
                    nbrs.append(self.grid[nr][nc])
        return nbrs

    def reveal(
        self, row: int | tuple[int, int], col: Optional[int] = None, flood: bool = False
    ) -> None:
        if col is None and isinstance(row, tuple):
            row, col = row
        cell = self.grid[row][col]
        if cell.state == State.HIDDEN:
            cell.state = State.REVEALED
            self.last_safe_reveal = (row, col)  # Update the last safe reveal position
            if flood and cell.adjacent_mines == 0:
                for neighbor in self.neighbors(row, col):
                    self.reveal(neighbor.row, neighbor.col, flood=True)

    def flag(self, row: int | tuple[int, int], col: Optional[int] = None) -> None:
        if col is None and isinstance(row, tuple):
            row, col = row
        cell = self.grid[row][col]
        if cell.state == State.HIDDEN:
            cell.state = State.FLAGGED

    @staticmethod
    def _from_token(token: str) -> Cell:
        if token == "hidden":
            return Cell(state=State.HIDDEN)
        elif token == "mine":
            return Cell(is_mine=True)
        return Cell()

    def add_cell(self, row, col, is_mine=False):
        """
        Add a cell to the board at the specified position, dynamically resizing if needed.

        :param row: Row index of the cell.
        :param col: Column index of the cell.
        :param is_mine: Whether the cell is a mine.
        """
        # Expand rows if necessary
        while row >= self.n_rows:
            self.grid.append(
                [
                    Cell(row=len(self.grid), col=c, state=State.HIDDEN)
                    for c in range(self.n_cols)
                ]
            )
            self.n_rows += 1

        # Expand columns if necessary
        for r in range(self.n_rows):
            while col >= self.n_cols:
                self.grid[r].append(
                    Cell(row=r, col=len(self.grid[r]), state=State.HIDDEN)
                )
            self.n_cols = max(self.n_cols, col + 1)

        # Add the new cell
        self.grid[row][col] = Cell(row=row, col=col, is_mine=is_mine)

    def get_neighbors(self, cell):
        """Get neighboring cells for a given cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = cell.row + dr, cell.col + dc
                if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                    neighbors.append(self.grid[r][c])
        return neighbors

    def solve_next(self):
        """Solve the next move on the board."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and cell.state == State.HIDDEN:
                    cell.state = State.REVEALED
                    return cell.row, cell.col
        raise RuntimeError("No moves left to solve.")

    def hidden_cells(self) -> list[Cell]:
        """Return a list of all hidden Cell objects."""
        hidden_cells = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell.state and cell.state.value == State.HIDDEN.value:
                    hidden_cells.append(cell)
        return hidden_cells

    @property
    def mines_remaining(self) -> int:
        """Return the number of mines remaining on the board."""
        total_mines = sum(cell.is_mine for row in self.grid for cell in row)
        flagged_mines = sum(
            cell.state == State.FLAGGED for row in self.grid for cell in row
        )
        return total_mines - flagged_mines

    @mines_remaining.setter
    def mines_remaining(self, value: int) -> None:
        if value < 0:
            raise ValueError("Mines remaining cannot be negative.")
        self._mines_remaining = value

    def adjacent_cells(self, row: int, col: int) -> list[tuple[int, int]]:
        """Return a list of coordinates for all adjacent cells."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                    neighbors.append((r, c))
        return neighbors

    def is_flagged(self, r: int | Cell, c: int | None = None) -> bool:
        """Check if a cell is flagged."""
        if isinstance(r, Cell):
            return r.state is State.FLAGGED
        return self.grid[r][c].state is State.FLAGGED

    def is_hidden(self, r: int | Cell, c: int | None = None) -> bool:
        """Check if a cell is hidden."""
        if isinstance(r, Cell):
            return r.state is State.HIDDEN
        return self.grid[r][c].state is State.HIDDEN

    def flag(self, r: int | Cell, c: int | None = None) -> None:
        """Flag a cell as a mine."""
        if isinstance(r, Cell):
            r.state = State.FLAGGED
        else:
            self.grid[r][c].state = State.FLAGGED

    def revealed_cells(self):
        """Return all revealed cells."""
        return [
            cell for row in self.grid for cell in row if cell.state == State.REVEALED
        ]

    def print_board(self):
        """Print the board for debugging purposes."""
        for row in self.grid:
            print("".join(str(cell) for cell in row))

    def clue(self, cell) -> int:
        """Return the clue value for a given cell."""
        return cell.clue

    def log_state(self, hypothesis_id, action, confidence):
        """Log the current board state to a .jsonl file with session-scoped rotation."""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"observer_state_log_{session_id}.jsonl"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "hypothesis_id": hypothesis_id,
            "action": action,  # e.g., 'flagged' or 'clicked'
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

    def has_unresolved_cells(self) -> bool:
        """
        Check if there are any hidden cells remaining on the board.

        Returns:
            bool: True if there are hidden cells, False otherwise.
        """
        for row in self.grid:
            for cell in row:
                if cell.state == State.HIDDEN:
                    return True
        return False

    def __getitem__(self, pos: tuple[int, int]) -> Cell:
        """
        Allow grid-style access to the board.

        Args:
            pos (tuple[int, int]): A tuple containing row and column indices.

        Returns:
            Cell: The cell at the specified position.
        """
        r, c = pos
        if not (0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])):
            raise IndexError("Board access out of bounds.")
        return self.grid[r][c]

    def __repr__(self):
        return f"Board(rows={self.n_rows}, cols={self.n_cols})"

    def get_revealed_hypotheses(self):
        """Returns a list of revealed hypotheses on the board."""
        return []

    def ensure_row_attribute(self):
        """Ensure all cells in the grid have a .row attribute."""
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.row = i
                cell.col = j

    def is_mine(self, cell):
        """Check if a cell is a mine."""
        return cell.is_mine

    def is_valid(self):
        """
        Check if the board is in a valid state by verifying clue consistency.

        :return: True if the board is valid, False otherwise.
        """
        for row in self.grid:
            for cell in row:
                if cell.state == State.REVEALED and cell.clue is not None:
                    # Count neighboring mines
                    neighbors = self.get_neighbors(cell)
                    mine_count = sum(1 for neighbor in neighbors if neighbor.is_mine)
                    if mine_count != cell.clue:
                        return False
        return True

    def is_solved(self):
        """Check if the board is solved."""
        return all(
            cell.is_mine or cell.state == State.REVEALED
            for row in self.grid
            for cell in row
        )

    def export_state(self) -> list[dict]:
        """
        Export the current board state as a list of dictionaries.

        :return: A list of dictionaries with cell details.
        """
        return [
            {
                "row": cell.row,
                "col": cell.col,
                "state": cell.state.name,
                "clue": cell.clue,
                "risk": getattr(cell, "risk", None),
            }
            for row in self.grid
            for cell in row
        ]

    def get_current_confidence(self) -> float:
        """
        Get the current confidence level.

        :return: The mean confidence level.
        """
        return BetaConfidence.mean()

    def is_hidden(self, cell_or_coords) -> bool:
        """
        Check if a cell is hidden.

        :param cell_or_coords: A Cell object or (row, col) tuple.
        :return: True if the cell is hidden, False otherwise.
        """
        if isinstance(cell_or_coords, Cell):
            return cell_or_coords.state == State.HIDDEN
        row, col = cell_or_coords
        return self.grid[row][col].state == State.HIDDEN

    def is_flagged(self, cell_or_coords) -> bool:
        """
        Check if a cell is flagged.

        :param cell_or_coords: A Cell object or (row, col) tuple.
        :return: True if the cell is flagged, False otherwise.
        """
        if isinstance(cell_or_coords, Cell):
            return cell_or_coords.state == State.FLAGGED
        row, col = cell_or_coords
        return self.grid[row][col].state == State.FLAGGED

    def flag(self, cell_or_coords) -> None:
        """
        Flag a cell.

        :param cell_or_coords: A Cell object or (row, col) tuple.
        """
        if isinstance(cell_or_coords, Cell):
            cell_or_coords.state = State.FLAGGED
        else:
            row, col = cell_or_coords
            self.grid[row][col].state = State.FLAGGED

    def expand_grid(self, new_rows: int, new_cols: int) -> None:
        """
        Expands the board grid to the specified dimensions.

        :param new_rows: The new number of rows.
        :param new_cols: The new number of columns.
        """
        if new_rows < self.n_rows or new_cols < self.n_cols:
            raise ValueError("New dimensions must be greater than or equal to current dimensions.")

        # Add new rows if necessary
        for i in range(self.n_rows, new_rows):
            new_row = [Cell(row=i, col=j, state=State.HIDDEN) for j in range(new_cols)]
            self.grid.append(new_row)

        # Expand existing rows to the new column count
        for i, row in enumerate(self.grid):
            for j in range(len(row), new_cols):
                row.append(Cell(row=i, col=j, state=State.HIDDEN))

        # Update board dimensions
        self.n_rows = new_rows
        self.n_cols = new_cols

        # Update neighbors for all cells
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.neighbors = self.adjacent_cells(i, j)
