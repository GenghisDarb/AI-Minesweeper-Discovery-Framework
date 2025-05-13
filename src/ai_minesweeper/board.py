from .cell import Cell

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

    def reveal(self, r, c):
        # Placeholder: reveal logic
        self.grid[r][c].state = self.grid[r][c].state  # No-op for now
