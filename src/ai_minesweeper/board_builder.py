from pathlib import Path
from ai_minesweeper.cell import Cell, State
from .board import Board


class BoardBuilder:
    """Factory helpers for Board objects."""

    def __init__(self) -> None:
        self.grid: list[list[str]] = []
        self.n_rows: int = 0
        self.n_cols: int = 0

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

    @staticmethod
    def from_ascii(ascii_str: str) -> "BoardBuilder":
        """Create a builder from a newline-separated ASCII grid.

        Symbols:
            • digit 0-8 → revealed clue
            • '.'       → hidden, empty
            • '*' or '#'→ hidden mine
        """
        def char_to_cell(ch: str) -> Cell:
            if ch.isdigit():
                return Cell(state=State.REVEALED, clue=int(ch), is_mine=False)
            if ch in ('.', ' '):
                return Cell(state=State.HIDDEN,  clue=0,        is_mine=False)
            if ch in ('*', '#'):
                return Cell(state=State.HIDDEN,  clue=0,        is_mine=True)
            raise ValueError(f"Unrecognized board char: {ch!r}")

        rows = [[char_to_cell(ch) for ch in line]
                for line in ascii_str.strip().splitlines()]

        bb = BoardBuilder()
        bb.grid   = rows
        bb.n_rows = len(rows)
        bb.n_cols = len(rows[0])
        return bb

    def build(self) -> "Board":
        """Finalize and return a fully populated Board instance."""
        from ai_minesweeper.board import Board   # local import to avoid cycle

        board = Board(self.n_rows, self.n_cols)  # ctor wants only dims
        board.grid = self.grid                   # inject our parsed layout
        return board
