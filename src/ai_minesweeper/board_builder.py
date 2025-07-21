from pathlib import Path

import pandas as pd

from ai_minesweeper.board import Board, Cell, State


class BoardBuilder:
    """Factory helpers for Board objects."""

    @staticmethod
    def from_csv(path: str | Path, header: bool | None = None) -> Board:
        """
        Parse a CSV file into a Board object.

        :param path: Path to the CSV file.
        :param header: Whether the CSV file has a header row (True/False/None).
        """
        # Interpret header argument
        header_option = 0 if header else None
        df = pd.read_csv(path, header=header_option)

        # Convert DataFrame → grid of Cell objects
        grid: list[list[Cell]] = []
        for _, row in df.iterrows():
            cells: list[Cell] = []
            for token in row:
                token_str = "" if pd.isna(token) else str(token).strip()
                if token_str.upper() in {"X", "*", "MINE"}:  # Marked mine
                    cell = Cell(is_mine=True, state=State.HIDDEN)
                    cell.symbol = token_str  # Assign symbol for mines
                    cells.append(cell)
                elif token_str.isdigit() and 0 <= int(token_str) <= 8:  # Clue
                    cell = Cell(state=State.REVEALED, clue=int(token_str))
                    cells.append(cell)
                else:  # Safe hidden cell
                    cell = Cell(state=State.HIDDEN)
                    cell.symbol = token_str
                    cells.append(cell)
            grid.append(cells)

        # Defensive checks
        if not grid or not grid[0]:
            raise ValueError("CSV file is empty or malformed (no data rows).")
        row_len = len(grid[0])
        board = Board(n_rows=len(grid), n_cols=row_len, grid=grid)
        return board

    @staticmethod
    def _from_relational_csv(df: pd.DataFrame) -> Board:
        """Parse a relational CSV format where each row represents one cell."""
        # Find the required columns (case-insensitive)
        columns = {col.lower(): col for col in df.columns}

        if "cell" not in columns or "row" not in columns or "column" not in columns:
            raise ValueError(
                "Relational CSV must have 'cell', 'row', and 'column' columns"
            )

        cell_col = columns["cell"]
        row_col = columns["row"]
        col_col = columns["column"]

        # Find board dimensions
        max_row = int(df[row_col].max())
        max_col = int(df[col_col].max())
        n_rows = max_row + 1
        n_cols = max_col + 1

        # Create empty board
        board = BoardBuilder._empty_board(n_rows, n_cols)

        # Populate board from relational data
        for _, row_data in df.iterrows():
            r = int(row_data[row_col])
            c = int(row_data[col_col])
            cell_value = row_data[cell_col]

            # Bounds checking
            if r < 0 or r >= n_rows or c < 0 or c >= n_cols:
                raise ValueError(
                    f"Cell coordinates ({r}, {c}) out of bounds for board size {n_rows}x{n_cols}"
                )

            cell = board.grid[r][c]
            if pd.isna(cell_value) or str(cell_value).strip() in ["", "0"]:
                cell.state = State.HIDDEN
                cell.is_mine = False
            elif str(cell_value).strip() in ["1", "M", "X", "*"]:
                cell.state = State.HIDDEN  # Start hidden, can be revealed later
                cell.is_mine = True
            else:
                # Try to parse as integer clue
                try:
                    clue_value = int(cell_value)
                    cell.state = State.REVEALED
                    cell.adjacent_mines = clue_value
                    cell.is_mine = False
                except ValueError:
                    # Default to hidden empty cell
                    cell.state = State.HIDDEN
                    cell.is_mine = False

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
        rows = [line.split() for line in text.strip().splitlines()]
        if not rows or not rows[0]:
            # Handle empty text by creating a minimal 1x1 board
            return BoardBuilder._empty_board(1, 1)
        board = BoardBuilder._empty_board(len(rows), len(rows[0]))
        BoardBuilder._populate_board(board, rows)
        return board

    @staticmethod
    def from_pdf(path: str) -> Board:
        """Parse a PDF file into a Board object."""
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
        return BoardBuilder.from_text(text)

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
                cell.adjacent_mines = sum(
                    1 for neighbor in neighbors if neighbor.is_mine
                )

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

    @classmethod
    def from_manual(
        cls, grid: list[list[str | int]], *, invalidate: bool = True
    ) -> "Board":
        """
        Build a Board directly from an in-memory grid.

        grid: 2-D list where each element is
              - "M" or "X"  → mine
              - "" or "."   → hidden empty
              - 0-8 (int)   → pre-revealed clue
        invalidate: if True, verify clue numbers
        """
        if invalidate:
            cls._validate_grid(grid)
        board = cls._empty_board(len(grid), len(grid[0]))
        cls._populate_board(board, grid)
        return board

    @staticmethod
    def _validate_grid(grid: list[list[str | int]]) -> None:
        """
        Validate the grid for consistency.

        Ensures that:
        - Clue numbers (0-8) are valid.
        - Mines are marked as "M" or "X".
        - Empty cells are "" or ".".
        """
        for row in grid:
            for cell in row:
                if isinstance(cell, int) and not (0 <= cell <= 8):
                    raise ValueError(f"Invalid clue number: {cell}")
                if isinstance(cell, str) and cell not in {"M", "X", "", "."}:
                    raise ValueError(f"Invalid cell value: {cell}")

    @staticmethod
    def _empty_board(rows: int, cols: int) -> Board:
        """
        Create an empty board with the specified dimensions.

        All cells are initialized as hidden and empty.
        """
        grid = [[Cell(state=State.HIDDEN) for _ in range(cols)] for _ in range(rows)]
        board = Board(grid=grid)
        return board

    @staticmethod
    def _populate_board(board: Board, grid: list[list[str | int]]) -> None:
        """
        Populate the board with cells based on the provided grid.

        grid: 2-D list where each element is
              - "M" or "X"  → mine
              - "" or "."   → hidden empty
              - 0-8 (int)   → pre-revealed clue
        """
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                cell = board.grid[r][c]
                if isinstance(value, Cell):
                    cell.symbol = value.symbol  # Preserve the symbol attribute
                elif str(value).upper() in {"MINE", "M", "X"}:
                    cell.is_mine = True
                elif isinstance(value, int):
                    cell.state = State.REVEALED
                    cell.adjacent_mines = value
                elif str(value).strip().upper() in {"", "."}:
                    cell.state = State.HIDDEN
                elif str(value).upper() == "HIDDEN":
                    cell.state = State.HIDDEN
                else:
                    raise ValueError(f"Invalid cell value: {value}")

        # Safety checks for list accesses
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                if r < len(board.grid) and c < len(board.grid[r]):
                    cell = board.grid[r][c]
                    if cell:
                        cell.neighbors = [
                            board.grid[x][y]
                            for x in range(max(0, r - 1), min(board.n_rows, r + 2))
                            for y in range(max(0, c - 1), min(board.n_cols, c + 2))
                            if (x, y) != (r, c)
                            and x < len(board.grid)
                            and y < len(board.grid[x])
                        ]

        # Check if rows is empty before accessing len(rows[0])
        if not grid or not grid[0]:
            raise ValueError("The provided text does not contain a valid board layout.")

    @staticmethod
    def empty_board(rows: int, cols: int) -> Board:
        """
        Create an empty board with the specified dimensions.

        :param rows: Number of rows in the board.
        :param cols: Number of columns in the board.
        :return: A Board object with all cells hidden and no mines.
        """
        grid = [[Cell(state=State.HIDDEN) for _ in range(cols)] for _ in range(rows)]
        return Board(n_rows=rows, n_cols=cols, grid=grid)
