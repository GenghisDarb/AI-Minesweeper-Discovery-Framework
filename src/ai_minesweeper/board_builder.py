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

        # compute weighted adjacent-mine counts
        for r in range(n_rows):
            for c in range(n_cols):
                cell = board.grid[r][c]
                if cell.is_mine:
                    cell.adjacent_mine_weight = -1
                    continue
                neighbours = board.neighbors(r, c)
                cell.adjacent_mine_weight = sum(
                    1 if n.row == r or n.col == c else 0.5
                    for n in neighbours if n.is_mine
                )

        return board

    @staticmethod
    def from_relations(relations: list[tuple[str, str]], false_hypotheses: list[str] | None = None) -> Board:
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
            import fitz  # PyMuPDF
            pdf_text = "\n".join(page.get_text() for page in fitz.open(stream=file_bytes, filetype="pdf"))
            return BoardBuilder.from_text(pdf_text)
        except ImportError:
            raise RuntimeError("PyMuPDF is required to parse PDF files.")
