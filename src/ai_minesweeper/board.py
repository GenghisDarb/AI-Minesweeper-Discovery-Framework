from .cell import Cell, State  # re-export so tests can import State here
import json
from datetime import datetime

__all__ = ["Board", "State"]  # optional but nice


class Board:
    def __init__(self, n_rows=None, n_cols=None, grid=None):
        if isinstance(grid, list):
            self.grid = [[Cell.from_token(token) for token in row] for row in grid]
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    cell.row = i
                    cell.col = j
            self.n_rows = len(grid)
            self.n_cols = len(grid[0]) if self.n_rows > 0 else 0
        elif n_rows is not None and n_cols is not None:
            self.n_rows = n_rows
            self.n_cols = n_cols
            self.grid = [
                [Cell(row=i, col=j) for j in range(n_cols)] for i in range(n_rows)
            ]
        elif grid is None:
            self.n_rows = 0
            self.n_cols = 0
            self.grid = []
        else:
            raise ValueError("Either grid or n_rows and n_cols must be provided.")
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
        print("[DEBUG] Board initialized with grid:")
        for row in self.grid:
            print(" ".join(cell.state.name for cell in row))

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

    def reveal(self, row: int, col: int, flood: bool = False) -> None:
        cell = self.grid[row][col]
        if cell.state != State.HIDDEN:
            return  # Skip already revealed or flagged cells
        cell.state = State.REVEALED
        self.last_safe_reveal = (row, col)  # Update the last safe reveal position
        if flood and cell.adjacent_mines == 0:
            for neighbor in self.neighbors(row, col):
                self.reveal(neighbor.row, neighbor.col, flood=True)

    def flag(self, row: int, col: int) -> None:
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
        """Add a cell to the board at the specified position."""
        if row >= self.n_rows or col >= self.n_cols:
            raise ValueError("Cell position out of bounds.")
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
        print("[DEBUG] Checking hidden cells...")
        print(f"[DEBUG] State.HIDDEN id: {id(State.HIDDEN)}")
        hidden = []
        for row in self.grid:
            for cell in row:
                print(f"[DEBUG] Cell at ({cell.row}, {cell.col}): State={cell.state}, State id={id(cell.state)}, Match with HIDDEN={cell.state == State.HIDDEN}")
                if cell.state == State.HIDDEN:
                    hidden.append(cell)
        print(f"[DEBUG] Total hidden cells found: {len(hidden)}")
        return hidden

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

    def is_flagged(self, cell: tuple[int, int]) -> bool:
        """Check if a cell is flagged."""
        r, c = cell
        return self.grid[r][c].state == State.FLAGGED

    def is_hidden(self, cell: tuple[int, int]) -> bool:
        """Check if a cell is hidden."""
        r, c = cell
        return self.grid[r][c].state == State.HIDDEN

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
        return self.grid[r][c]
