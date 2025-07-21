from ai_minesweeper.board import Board

from ..cell import State


class NuclearIsotopeAdapter:
    NAME = "periodic-table-v2"

    def build_board(self, csv_path="examples/periodic_table/isotopes.csv"):
        """
        Build a Minesweeper board for nuclear isotopes.
        :param csv_path: Path to the isotopes CSV file.
        """
        from pathlib import Path

        import pandas as pd

        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(
                "Isotopes CSV file missing. Run scripts/fetch_nubase_subset.py to download isotopes.csv."
            )

        # Load isotopes data
        df = pd.read_csv(csv_path)

        # Initialize board dimensions
        max_z = df["Z"].max()
        max_n = df["N"].max()
        board = Board(n_rows=max_z + 1, n_cols=max_n + 1)

        for _, row in df.iterrows():
            z, n = row["Z"], row["N"]
            is_mine = row["IsStable"] == "F" or row["QαMeV"] < 0
            board.add_cell(z, n, is_mine=is_mine)

        # Flag mines
        for row in board.grid:
            for cell in row:
                if cell.is_mine:
                    cell.state = State.FLAGGED

        # Compute weighted clues
        for cell in board.cells:
            neighbors = board.get_neighbors(cell)
            cell.adjacent_mine_weight = sum(
                1 if neighbor.z == cell.z or neighbor.n == cell.n else 0.5
                for neighbor in neighbors
                if neighbor.is_mine
            )

        return board
