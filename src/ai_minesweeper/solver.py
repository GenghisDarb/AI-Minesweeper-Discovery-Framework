from .click_engine import ClickEngine
from .board import Board


class ConstraintSolver:
    """Very small loop that keeps clicking until max_moves."""

    @staticmethod
    def solve(board: Board, max_moves: int = 10) -> None:
        for _ in range(max_moves):
            r, c = ClickEngine.next_click(board)
            board.reveal(r, c)

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
                cell: Cell = board.grid[r][c]
                if token == "*":
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
