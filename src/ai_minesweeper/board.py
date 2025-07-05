from .cell import Cell, State   # re-export so tests can import State here
__all__ = ["Board", "State"]    # optional but nice

class Board:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[Cell() for _ in range(n_cols)] for _ in range(n_rows)]
        self.custom_neighbors: dict[tuple[int, int], list[tuple[int, int]]] | None = None  # Logical neighbor map

    def neighbors(self, r, c):
        if self.custom_neighbors is not None:
            return [self.grid[nr][nc] for (nr, nc) in self.custom_neighbors.get((r, c), [])]
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
