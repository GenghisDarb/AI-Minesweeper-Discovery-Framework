from .cell import Cell, State  # re-export so tests can import State here

__all__ = ["Board", "State"]  # optional but nice


class Board:
    def __init__(self, n_rows=None, n_cols=None, grid=None):
        if isinstance(grid, list):
            self.grid = [[Cell.from_token(token) for token in row] for row in grid]
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
        self.custom_neighbors: dict[tuple[int, int], list[tuple[int, int]]] | None = (
            None  # Logical neighbor map
        )

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
