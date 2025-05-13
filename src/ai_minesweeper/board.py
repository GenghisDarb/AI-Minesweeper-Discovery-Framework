from .cell import Cell, State   # re-export so tests can import State here
__all__ = ["Board", "State"]    # optional but nice

class Board:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[Cell() for _ in range(n_cols)] for _ in range(n_rows)]

    def neighbors(self, r, c):
        # Placeholder: returns list of neighbor cells
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
        """
        Reveal the cell at (row, col).
        If `flood` is True, recursively reveal neighboring empty cells (classic Minesweeper flood-fill).
        Placeholder logic: just mark the target cell as REVEALED.
        """
        cell = self.grid[row][col]
        cell.state = State.REVEALED
        # TODO: implement real flood logic
