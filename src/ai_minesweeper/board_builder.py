from pathlib import Path
from .board import Board, Cell, State


class BoardBuilder:
    """Factory helpers for Board objects."""

    @staticmethod
    def from_csv(path: str | Path) -> Board:
        """Parse a CSV file of `*` (mine) and `.` (empty) into a Board object."""
        path = Path(path)
        rows = [line.strip().split(",") for line in path.read_text().strip().splitlines()]
        n_rows, n_cols = len(rows), len(rows[0])

        board = Board(n_rows, n_cols)

        # mark mines
        for r, line in enumerate(rows):
            for c, token in enumerate(line):
                token = token.strip()
                cell: Cell = board.grid[r][c]
                if "*" in token:               # ← accept any cell that contains '*'
                    cell.is_mine = True
                cell.state = State.HIDDEN  # ensure consistent state

        # compute adjacent‐mine counts
        for r in range(n_rows):
            for c in range(n_cols):
                cell = board.grid[r][c]
                if cell.is_mine:
                    cell.adjacent_mines = -1
                    continue
                neighbours = board.neighbors(r, c)
                cell.adjacent_mines = sum(1 for n in neighbours if n.is_mine)

        return board
