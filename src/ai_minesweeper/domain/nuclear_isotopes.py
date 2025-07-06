from ai_minesweeper.board import Board

class NuclearIsotopeAdapter:
    NAME = "periodic-table-v2"

    def build_board(self, csv_path="examples/periodic_table/isotopes.csv"):
        """
        Build a Minesweeper board for nuclear isotopes.
        :param csv_path: Path to the isotopes CSV file.
        """
        import pandas as pd

        # Load isotopes data
        df = pd.read_csv(csv_path)

        # Initialize board
        board = Board()

        for _, row in df.iterrows():
            z, n = row["Z"], row["N"]
            is_mine = row["IsStable"] == "F" or row["QαMeV"] < 0
            board.add_cell(z, n, is_mine=is_mine)

        # Compute weighted clues
        for cell in board.cells:
            neighbors = board.get_neighbors(cell)
            cell.adjacent_mine_weight = sum(
                1 if neighbor.z == cell.z or neighbor.n == cell.n else 0.5
                for neighbor in neighbors if neighbor.is_mine
            )

        return board
