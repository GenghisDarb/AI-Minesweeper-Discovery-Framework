from pathlib import Path
from .board import Board, Cell, State


class BoardBuilder:
    """Factory helpers for Board objects."""

    @staticmethod
    def from_csv(path: str | Path) -> Board:
        import pandas as pd

        df = pd.read_csv(path, header=None)  # Adjusted to handle CSVs without headers
        print(f"CSV DataFrame: {df}")  # Debugging output
        grid = []

        for _, row in df.iterrows():
            row_cells = []
            for token in row:
                token_str = str(token).strip() if not pd.isna(token) else ""
                # Refined mine detection logic
                is_mine = token_str in {"1", "*", "mine"}  # Adjusted to match test cases
                row_cells.append(Cell(state=State.HIDDEN, is_mine=is_mine, symbol=token_str))
            grid.append(row_cells)

        # Adjust dimensions to match expected test cases
        n_rows = len(grid)
        n_cols = max(len(row) for row in grid)
        board = Board(n_rows=n_rows, n_cols=n_cols)
        board.grid = grid

        # Ensure all rows have consistent column count
        for row in grid:
            while len(row) < n_cols:
                row.append(Cell(state=State.HIDDEN))

        # Debugging output for board dimensions
        print(f"Board dimensions: {n_rows} rows, {n_cols} columns")

        # Compute adjacent mine counts
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.is_mine:
                    cell.adjacent_mines = -1
                    continue
                neighbors = board.neighbors(r, c)
                cell.adjacent_mines = sum(neighbor.is_mine for neighbor in neighbors)

        # Set row and column attributes for each cell
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                cell.row = r
                cell.col = c

        return board

    @staticmethod
    def from_relations(
        relations: list[tuple[str, str]], false_hypotheses: list[str] | None = None
    ) -> Board:
        """
        Build a Board from a list of hypothesis relations and known false hypotheses.
        """
        false_hypotheses = false_hypotheses or []
        hypotheses = set(h for relation in relations for h in relation)
        n = len(hypotheses)
        n_rows = n_cols = int(n**0.5) + (1 if n**0.5 % 1 else 0)

        board = Board(n_rows, n_cols)
        hypothesis_map = {}

        # Assign hypotheses to cells
        for i, hypothesis in enumerate(hypotheses):
            r, c = divmod(i, n_cols)
            cell = board.grid[r][c]
            cell.description = hypothesis
            cell.is_mine = hypothesis in false_hypotheses
            hypothesis_map[hypothesis] = (r, c)

        # Define custom neighbors
        board.custom_neighbors = {}
        for h1, h2 in relations:
            r1, c1 = hypothesis_map[h1]
            r2, c2 = hypothesis_map[h2]
            board.custom_neighbors.setdefault((r1, c1), []).append((r2, c2))
            board.custom_neighbors.setdefault((r2, c2), []).append((r1, c1))

        return board

    @staticmethod
    def from_text(text: str) -> Board:
        """Parse raw text into a Board object."""
        if not text.strip():
            return Board(grid=[])  # Return an empty board for empty text

        rows = [line.strip().split() for line in text.strip().splitlines()]
        n_rows, n_cols = len(rows), len(rows[0])

        board = Board(n_rows, n_cols)

        for r, line in enumerate(rows):
            for c, token in enumerate(line):
                token = token.strip()
                cell: Cell = board.grid[r][c]
                if "mine" in token:
                    cell.is_mine = True
                cell.state = State.HIDDEN

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
    def from_pdf(file_bytes: bytes) -> Board:
        """Parse a PDF file into a Board object."""
        try:
            import pdfplumber

            with pdfplumber.open(file_bytes) as pdf:
                pdf_text = "\n".join(page.extract_text() for page in pdf.pages)
            return BoardBuilder.from_text(pdf_text)
        except ImportError:
            raise RuntimeError("pdfplumber is required to parse PDF files.")

    @staticmethod
    def random_board(rows: int, cols: int, mines: int) -> Board:
        """Generate a random board with the specified dimensions and number of mines."""
        import random

        board = Board(rows, cols)
        mine_positions = random.sample(range(rows * cols), mines)

        for pos in mine_positions:
            r, c = divmod(pos, cols)
            board.grid[r][c].is_mine = True

        for r in range(rows):
            for c in range(cols):
                cell = board.grid[r][c]
                if cell.is_mine:
                    cell.adjacent_mines = -1
                    continue
                neighbors = board.neighbors(r, c)
                cell.adjacent_mines = sum(1 for neighbor in neighbors if neighbor.is_mine)

        return board

    @staticmethod
    def fixed_board(layout, mines):
        n_rows = len(layout)
        n_cols = len(layout[0])
        grid = []

        for r, row in enumerate(layout):
            grid_row = []
            for c, char in enumerate(row):
                if (r, c) in mines:
                    grid_row.append(Cell(is_mine=True, state=State.HIDDEN))
                else:
                    grid_row.append(Cell(state=State.HIDDEN))
            grid.append(grid_row)

        board = Board(n_rows=n_rows, n_cols=n_cols, grid=grid)

        # Initialize neighbors
        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                cell.neighbors = [
                    board.grid[x][y]
                    for x in range(max(0, i - 1), min(board.n_rows, i + 2))
                    for y in range(max(0, j - 1), min(board.n_cols, j + 2))
                    if (x, y) != (i, j)
                ]

        # Calculate and set correct clue values
        for i, row in enumerate(board.grid):
            for j, cell in enumerate(row):
                cell.clue = sum(neighbor.is_mine for neighbor in cell.neighbors)

        return board
