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
from typing import List, Optional, Tuple, Iterable, Any
from enum import Enum

from ai_minesweeper.constants import DEBUG

from .cell import Cell as _Cell, State  # re‑export so tests can import State here
# Re-export Cell under expected name
Cell = _Cell

__all__ = ["Board", "Cell", "State", "CellState"]

PathHistory = List[Tuple[int, int]]


class CellState(Enum):
    """Cell states in the minesweeper board."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    SAFE_FLAGGED = "safe_flagged"  # χ‑recursive safe flag


class Board:
    """Core board class implementing χ‑recursive Minesweeper logic.

    This class had drift with duplicate constructors / reveal methods; it is
    now normalized to a single coherent API expected by risk/constraint tests.
    """

    def __init__(self, n_rows: Optional[int] = None, n_cols: Optional[int] = None, mine_count: Optional[int] = None, grid: Optional[Iterable] = None):
        # Support construction either from explicit dimensions or a provided grid of Cell objects
        if grid is not None:
            if not (isinstance(grid, list) and all(isinstance(row, list) for row in grid)):
                raise TypeError("grid must be a 2D list")
            # Normalize tokens to Cell objects if needed
            normalized_grid: List[List[_Cell]] = []
            for r, row in enumerate(grid):
                norm_row: List[_Cell] = []
                for c, item in enumerate(row):
                    if isinstance(item, _Cell):
                        cell = item
                    else:
                        # Convert token/str to Cell
                        cell = _Cell.from_token(item)
                        # Promote token mines to is_mine=True
                        if getattr(cell, "state", None) and str(cell.state) == State.MINE.value:
                            cell.is_mine = True
                    cell.row = r
                    cell.col = c
                    if not hasattr(cell, "state") or cell.state is None:
                        cell.state = State.HIDDEN
                    norm_row.append(cell)
                normalized_grid.append(norm_row)
            self.grid = normalized_grid
            self.n_rows = len(self.grid)
            self.n_cols = len(self.grid[0]) if self.n_rows else 0
            # Preserve the declared mine count separately from dynamic counting
            self._declared_mine_count = sum(getattr(c, 'is_mine', False) for row in self.grid for c in row)
        else:
            # Accept mine_count as optional; require integer n_rows and n_cols
            if not (isinstance(n_rows, int) and isinstance(n_cols, int)):
                raise TypeError("Provide either grid or integer n_rows and n_cols")
            self.n_rows = int(n_rows)  # type: ignore[arg-type]
            self.n_cols = int(n_cols)  # type: ignore[arg-type]
            self._declared_mine_count = int(mine_count) if isinstance(mine_count, int) else 0
            # Initialize with default non-mine cells
            self.grid = [[_Cell(is_mine=False) for _ in range(self.n_cols)] for _ in range(self.n_rows)]

        if self._declared_mine_count is not None and self._declared_mine_count > (self.n_rows * self.n_cols):
            raise ValueError("Mine count exceeds total cells")

        # neighbor cache / overrides
        self.custom_neighbors = {}  # type: ignore[assignment]

        # mines container and safe flags (for legacy/compat APIs)
        self.mines: set[tuple[int, int]] = set()
        self.safe_flags: set[tuple[int, int]] = set()

        # Initialize cell coordinate metadata (idempotent if already set)
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                setattr(cell, 'row', i)
                setattr(cell, 'col', j)
                if not hasattr(cell, 'state'):
                    from .cell import State as CellStateInternal
                    cell.state = CellStateInternal.HIDDEN

        # χ / confidence tracking
        self.last_safe_reveal = None  # last safe reveal position
        self.confidence_history = []  # rolling confidence values
        self.chi_cycle_count = 0
        self._mines_remaining_override = None

        if DEBUG:
            print(f"[BOARD INIT] rows={self.n_rows} cols={self.n_cols} declared_mines={self._declared_mine_count}")

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
        """Return a flattened list of all cells on the board."""
        return [cell for row in self.grid for cell in row]

    # -------------------------------------------------------------------------
    # Neighbor handling
    # -------------------------------------------------------------------------
    def neighbors(self, r: int, c: int) -> List[Cell]:
        """Return the list of neighboring Cell objects for the cell at (r, c)."""
        if not hasattr(self, 'custom_neighbors'):
            self.custom_neighbors = {}

        if self.custom_neighbors:
            coords = self.custom_neighbors.get((r, c), [])
            return [self.grid[nr][nc] for (nr, nc) in coords if 0 <= nr < self.n_rows and 0 <= nc < self.n_cols]

        nbrs: List[Cell] = []
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
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
    def reveal(self, pos: tuple[int, int] | int | Cell, col: Optional[int] = None, flood: bool = False, visited: Optional[set[tuple[int, int]]] = None) -> None:
        """Reveal a cell. If flood=True and the revealed cell has clue 0, perform an iterative BFS flood to reveal contiguous zero regions.

        Accepts either (row, col) tuple or row, col ints.
        """
        if visited is None:
            visited = set()
        # Normalize inputs (accept tuple, row+col ints, or Cell-like)
        if col is None and isinstance(pos, tuple):
            row, col = pos
        elif col is None and hasattr(pos, 'row') and hasattr(pos, 'col'):
            row = int(getattr(pos, 'row'))
            col = int(getattr(pos, 'col'))
        elif isinstance(pos, int) and col is not None:
            row = pos
        else:
            raise TypeError("reveal expects (row,col) tuple or row, col ints")

        row = int(row)  # type: ignore[arg-type]
        col = int(col)  # type: ignore[arg-type]

        def _reveal_cell(r: int, c: int) -> int:
            # Reveal a single non-mine cell if hidden; return its clue
            cell_local = self.grid[r][c]
            if getattr(cell_local, 'is_mine', False):
                # Never reveal mines via flood or accidental reveals
                return -1
            if getattr(cell_local, 'state', None) == State.HIDDEN:
                cell_local.state = State.REVEALED
                self.last_safe_reveal = (r, c)
                # OSQN tick on observation
                try:
                    self.tick_chi_cycle(confidence=0.5)
                except Exception:
                    self.chi_cycle_count += 1
            # Prefer explicit clue if available; fallback to adjacent_mines
            clue_val = getattr(cell_local, 'clue', None)
            if clue_val is None:
                clue_val = getattr(cell_local, 'adjacent_mines', 0)
            return int(clue_val or 0)

        # Always reveal the starting cell
        start_adj = _reveal_cell(row, col)

        # If not flooding or starting cell is non‑zero, we're done
        if not flood or start_adj != 0:
            return

        # Iterative BFS flood fill from zeros
        from collections import deque
        queue = deque()
        if (row, col) not in visited:
            visited.add((row, col))
        queue.append((row, col))

        while queue:
            r, c = queue.popleft()
            # For each zero cell, expand to neighbors
            cell_here = self.grid[r][c]
            if getattr(cell_here, 'is_mine', False):
                # Shouldn't happen from flood, but guard anyway
                continue
            adj_here = int((getattr(cell_here, 'clue', None) if getattr(cell_here, 'clue', None) is not None else getattr(cell_here, 'adjacent_mines', 0)) or 0)
            if adj_here != 0:
                # Numbered boundary: do not expand further
                continue
            for nr, nc in self.get_neighbors(r, c):
                if (nr, nc) in visited:
                    continue
                visited.add((nr, nc))
                # Reveal neighbor (non-mine) and enqueue if it's also zero
                adj = _reveal_cell(nr, nc)
                if adj == 0:
                    queue.append((nr, nc))

    # ---------------------------------------------------------------------
    # Compatibility shims expected by tests
    # ---------------------------------------------------------------------
    @property
    def width(self) -> int:
        return int(self.n_cols)

    @property
    def height(self) -> int:
        return int(self.n_rows)

    @property
    def remaining_mines(self) -> int:
        return int(self.mines_remaining)

    @property
    def cell_states(self) -> dict[tuple[int, int], CellState]:
        mapping: dict[tuple[int, int], CellState] = {}
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                st = getattr(self.grid[r][c], 'state', None)
                if st == State.REVEALED:
                    mapping[(r, c)] = CellState.REVEALED
                elif st == State.FLAGGED:
                    mapping[(r, c)] = CellState.FLAGGED
                else:
                    mapping[(r, c)] = CellState.HIDDEN
        # Mark safe flags
        for pos in getattr(self, 'safe_flags', set()):
            mapping[tuple(pos)] = CellState.SAFE_FLAGGED
        return mapping

    @property
    def revealed_numbers(self) -> dict[tuple[int, int], int]:
        nums: dict[tuple[int, int], int] = {}
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                cell = self.grid[r][c]
                if getattr(cell, 'state', None) == State.REVEALED:
                    val = getattr(cell, 'clue', None)
                    if val is None:
                        val = getattr(cell, 'adjacent_mines', 0)
                    nums[(r, c)] = int(val or 0)
        return nums

    def reveal_cell(self, r: int, c: int) -> bool:
        """Compatibility: reveal a cell and return True if it's not a mine."""
        r = int(r); c = int(c)
        # Treat as mine if annotated in either grid attribute or mines set
        if getattr(self.grid[r][c], 'is_mine', False) or (r, c) in getattr(self, 'mines', set()):
            return False
        self.reveal((r, c), flood=True)
        return True

    def flag_cell(self, r: int, c: int, safe_flag: bool = False) -> None:
        """Compatibility: flag a cell; if safe_flag True, mark as SAFE_FLAGGED."""
        r = int(r); c = int(c)
        if safe_flag:
            self.safe_flags.add((r, c))
            if getattr(self.grid[r][c], 'state', None) == State.HIDDEN:
                self.grid[r][c].state = State.FLAGGED
        else:
            self.flag(r, c)

    def flag(self, r: int, c: int) -> None:
        """Flag a cell as a mine deterministically (no peeking)."""
        r = int(r)
        c = int(c)
        cell = self.grid[r][c]
        if getattr(cell, 'state', None) == State.HIDDEN:
            cell.state = State.FLAGGED
            # Keep compatibility sets updated if used elsewhere
            try:
                self.safe_flags.discard((r, c))
            except Exception:
                pass
            # Tick chi cycle on mutation
            try:
                self.tick_chi_cycle(confidence=0.5)
            except Exception:
                self.chi_cycle_count += 1

    @property
    def mine_count(self) -> int:
        """Total mines on the board, preferring declared count else counting is_mine flags."""
        if isinstance(getattr(self, "_declared_mine_count", None), int) and self._declared_mine_count > 0:
            return int(self._declared_mine_count)
        return sum(1 for row in self.grid for cell in row if getattr(cell, 'is_mine', False))

    def tick_chi_cycle(self, confidence: float = 0.5) -> None:
        """Shim to advance chi cycle; delegates to update_chi_cycle if available."""
        try:
            self.update_chi_cycle(confidence)
        except Exception:
            # Fallback counter
            self.chi_cycle_count += 1
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
                    neighbors = self.get_neighbors(cell)  # type: ignore[arg-type]
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
    def get_neighbors(self, *args: Any) -> List[Any]:
        """Overloaded neighbor helper.

        - When called with (row:int, col:int) -> returns list[tuple[int,int]]
        - When called with (cell:Cell-like) -> returns list[Cell]
        """
        if len(args) == 2 and all(isinstance(x, int) for x in args):
            row, col = args  # type: ignore[assignment]
            coords: list[tuple[int, int]] = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                        coords.append((r, c))
            return coords
        elif len(args) == 1:
            cell = args[0]
            out: List[Any] = []
            r0, c0 = getattr(cell, 'row'), getattr(cell, 'col')
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    r, c = r0 + dr, c0 + dc
                    if 0 <= r < self.n_rows and 0 <= c < self.n_cols:
                        out.append(self.grid[r][c])
            return out
        else:
            raise TypeError("get_neighbors expects (row:int, col:int) or (cell)")

    # -------------------------------------------------------------------------
    # Mines and flagging
    # -------------------------------------------------------------------------
    @property
    def mines_remaining(self) -> int:
        flagged = sum(1 for row in self.grid for cell in row if getattr(cell, 'state', None) == State.FLAGGED)
        if self._mines_remaining_override is not None:
            # Treat override as total mines; compute remaining dynamically
            remaining = int(self._mines_remaining_override) - flagged
            return remaining if remaining >= 0 else 0
        # Prefer declared count if available
        total_mines = self.mine_count
        remaining = total_mines - flagged
        return remaining if remaining >= 0 else 0

    @mines_remaining.setter
    def mines_remaining(self, value: int) -> None:
        if value < 0:
            raise ValueError("Mines remaining cannot be negative")
        self._mines_remaining_override = value

    def solve_next(self):
        """Perform one deterministic action: prefer a logical flag, else safe reveal, else frontier reveal, else central reveal."""
        from ai_minesweeper.utils.dr import dr_sort

        # Helper: iterate revealed numbered cells deterministically
        def iter_number_cells():
            coords = []
            for r in range(self.n_rows):
                for c in range(self.n_cols):
                    cell = self.grid[r][c]
                    if getattr(cell, 'state', None) == State.REVEALED:
                        clue = getattr(cell, 'clue', getattr(cell, 'adjacent_mines', None))
                        if clue is not None:
                            coords.append((r, c))
            return dr_sort(coords)

        # 1) Classic constraint: flag if need equals number of hidden neighbors
        for (r, c) in iter_number_cells():
            clue = int(getattr(self.grid[r][c], 'clue', getattr(self.grid[r][c], 'adjacent_mines', 0)) or 0)
            neighbors = self.get_neighbors(r, c)
            hidden = [(nr, nc) for (nr, nc) in neighbors if self.grid[nr][nc].state == State.HIDDEN]
            if not hidden:
                continue
            flagged = [(nr, nc) for (nr, nc) in neighbors if self.grid[nr][nc].state == State.FLAGGED]
            need = clue - len(flagged)
            if need == len(hidden) and need > 0:
                nr, nc = dr_sort(hidden)[0]
                self.flag(nr, nc)
                return (nr, nc)

        # 2) Classic constraint: safe reveal if flagged equals clue
        for (r, c) in iter_number_cells():
            clue = int(getattr(self.grid[r][c], 'clue', getattr(self.grid[r][c], 'adjacent_mines', 0)) or 0)
            neighbors = self.get_neighbors(r, c)
            hidden = [(nr, nc) for (nr, nc) in neighbors if self.grid[nr][nc].state == State.HIDDEN]
            if not hidden:
                continue
            flagged = [(nr, nc) for (nr, nc) in neighbors if self.grid[nr][nc].state == State.FLAGGED]
            if len(flagged) == clue:
                nr, nc = dr_sort(hidden)[0]
                self.reveal((nr, nc), flood=True)
                return (nr, nc)

        # 3) Subset inference: adjacent numbers only
        number_cells = list(iter_number_cells())
        for idx_a in range(len(number_cells)):
            r1, c1 = number_cells[idx_a]
            cell1 = self.grid[r1][c1]
            clue1 = int(getattr(cell1, 'clue', getattr(cell1, 'adjacent_mines', 0)) or 0)
            n1 = self.get_neighbors(r1, c1)
            H1 = {(nr, nc) for (nr, nc) in n1 if self.grid[nr][nc].state == State.HIDDEN}
            F1 = {(nr, nc) for (nr, nc) in n1 if self.grid[nr][nc].state == State.FLAGGED}
            need1 = clue1 - len(F1)
            if need1 < 0:
                continue
            for idx_b in range(idx_a + 1, len(number_cells)):
                r2, c2 = number_cells[idx_b]
                if abs(r1 - r2) > 1 or abs(c1 - c2) > 1:
                    continue
                cell2 = self.grid[r2][c2]
                clue2 = int(getattr(cell2, 'clue', getattr(cell2, 'adjacent_mines', 0)) or 0)
                n2 = self.get_neighbors(r2, c2)
                H2 = {(nr, nc) for (nr, nc) in n2 if self.grid[nr][nc].state == State.HIDDEN}
                F2 = {(nr, nc) for (nr, nc) in n2 if self.grid[nr][nc].state == State.FLAGGED}
                need2 = clue2 - len(F2)
                if need2 < 0:
                    continue
                # H1 subset of H2 -> act on H2\H1
                if H1 and H1.issubset(H2):
                    diff = H2 - H1
                    if diff:
                        if need2 - need1 == len(diff):
                            nr, nc = dr_sort(list(diff))[0]
                            self.flag(nr, nc)
                            return (nr, nc)
                        if need2 - need1 == 0:
                            nr, nc = dr_sort(list(diff))[0]
                            self.reveal((nr, nc), flood=True)
                            return (nr, nc)
                # H2 subset of H1 -> act on H1\H2
                if H2 and H2.issubset(H1):
                    diff = H1 - H2
                    if diff:
                        if need1 - need2 == len(diff):
                            nr, nc = dr_sort(list(diff))[0]
                            self.flag(nr, nc)
                            return (nr, nc)
                        if need1 - need2 == 0:
                            nr, nc = dr_sort(list(diff))[0]
                            self.reveal((nr, nc), flood=True)
                            return (nr, nc)

        # 4) Frontier exploration fallback
        def count_revealed_number_neighbors(r: int, c: int) -> int:
            cnt = 0
            for (nr, nc) in self.get_neighbors(r, c):
                cell = self.grid[nr][nc]
                if getattr(cell, 'state', None) == State.REVEALED and getattr(cell, 'clue', getattr(cell, 'adjacent_mines', None)) is not None:
                    cnt += 1
            return cnt

        def hidden_neighbor_count(r: int, c: int) -> int:
            return sum(1 for (nr, nc) in self.get_neighbors(r, c) if self.grid[nr][nc].state == State.HIDDEN)

        hidden_cells = [(r, c) for r in range(self.n_rows) for c in range(self.n_cols) if self.grid[r][c].state == State.HIDDEN]
        frontier: list[tuple[int, int]] = []
        for (r, c) in hidden_cells:
            if count_revealed_number_neighbors(r, c) > 0:
                frontier.append((r, c))

        if frontier:
            def rank(t: tuple[int, int]):
                r, c = t
                return (
                    -count_revealed_number_neighbors(r, c),
                    hidden_neighbor_count(r, c),
                    r, c,
                )
            target = sorted(frontier, key=rank)[0]
            self.reveal(target, flood=True)
            return target

        # 5) No frontier yet: choose central hidden cell, fallback to dr_sort
        centers: list[tuple[int, int]] = []
        mid_r = self.n_rows // 2
        mid_c = self.n_cols // 2
        cand_rows = [mid_r] if self.n_rows % 2 == 1 else [mid_r - 1, mid_r]
        cand_cols = [mid_c] if self.n_cols % 2 == 1 else [mid_c - 1, mid_c]
        for rr in cand_rows:
            for cc in cand_cols:
                if 0 <= rr < self.n_rows and 0 <= cc < self.n_cols:
                    centers.append((rr, cc))
        center_hidden = [p for p in centers if self.grid[p[0]][p[1]].state == State.HIDDEN]
        target = dr_sort(center_hidden or hidden_cells)[0] if (center_hidden or hidden_cells) else None
        if target is None:
            return None
        self.reveal(target, flood=True)
        return target

    def is_hidden(self, cell_or_pos):
        if isinstance(cell_or_pos, tuple):
            r, c = cell_or_pos
            return self.grid[r][c].state == State.HIDDEN
        return cell_or_pos.state == State.HIDDEN

    def is_revealed(self, r: int, c: int) -> bool:
        return self.grid[r][c].state == State.REVEALED  # type: ignore[index]

    def get_adjacent_mines(self, r: int, c: int) -> int:
        # Use explicit mines set when available
        if self.mines:
            return sum(1 for (nr, nc) in self.get_neighbors(int(r), int(c)) if (nr, nc) in self.mines)
        return sum(1 for nbr in self.neighbors(r, c) if getattr(nbr, 'is_mine', False))

    def update_chi_cycle(self, confidence: float) -> None:
        self.confidence_history.append(confidence)
        self.chi_cycle_count += 1

    # (Removed duplicate __init__ that caused signature conflicts)

    def get_revealed_cells(self) -> List[Tuple[int, int]]:
        return [(cell.row, cell.col) for row in self.grid for cell in row if cell.state == State.REVEALED]

    def get_hidden_cells(self) -> List[Tuple[int, int]]:
        return [(cell.row, cell.col) for row in self.grid for cell in row if cell.state == State.HIDDEN]

    def get_flagged_cells(self) -> List[Tuple[int, int]]:
        return [(cell.row, cell.col) for row in self.grid for cell in row if cell.state == State.FLAGGED]

    # Note: Removed duplicate legacy solve_next; the single-action, frontier-biased solve_next above remains the canonical implementation.

    # ---------------------------------------------------------------------
    # Mine placement helpers (compat)
    # ---------------------------------------------------------------------
    def place_mines(self, first_click: Optional[tuple[int, int]] = None) -> None:
        """Populate self.mines with positions, avoiding first_click. No-op if already filled to mine_count."""
        avoid = set()
        if first_click is not None:
            avoid.add((int(first_click[0]), int(first_click[1])))
        # If already populated to declared count, do nothing
        if self.mines and len(self.mines) >= self.mine_count:
            return
        # Deterministic fill scan to reach mine_count
        needed = max(self.mine_count - len(self.mines), 0)
        if needed == 0:
            return
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                if needed == 0:
                    break
                if (r, c) in avoid or (r, c) in self.mines:
                    continue
                self.mines.add((r, c))
                # Also mark cell attribute for compatibility with dynamic checks
                self.grid[r][c].is_mine = True
                needed -= 1
            if needed == 0:
                break