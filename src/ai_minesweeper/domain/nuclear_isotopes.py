from ai_minesweeper.board import Board


class NuclearIsotopeAdapter:
    NAME = "periodic-table-v2"

    def build_board(self, csv_path="examples/periodic_table/isotopes.csv") -> Board:
        """
        Build a Minesweeper board for nuclear isotopes using the current Board API.
        Cells where the dataset indicates instability are treated as mines (hidden).
        """
        from pathlib import Path

        import pandas as pd

        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Isotopes CSV file missing: {csv_path}. Run scripts/fetch_nubase_subset.py if needed."
            )

        df = pd.read_csv(csv_path)
        # Cast to built-in int for robustness with numpy dtypes
        max_z = int(df["Z"].max())
        max_n = int(df["N"].max())
        board = Board(n_rows=max_z + 1, n_cols=max_n + 1)

        # Mark mines based on domain labels: unstable (IsStable == 'F') or negative QαMeV
        for _, row in df.iterrows():
            z = int(row["Z"])  # type: ignore[call-arg]
            n = int(row["N"])  # type: ignore[call-arg]
            is_unstable = False
            try:
                is_unstable = (str(row.get("IsStable", "")).upper() == "F")
            except Exception:
                pass
            q_alpha = row.get("QαMeV") if "QαMeV" in df.columns else row.get("QalphaMeV")
            q_alpha_val = None
            if q_alpha is not None and q_alpha != "" and q_alpha != "?":
                try:
                    q_alpha_val = float(q_alpha)
                except Exception:
                    q_alpha_val = None
            is_mine = is_unstable or (q_alpha_val is not None and q_alpha_val < 0)
            if is_mine:
                cell = board.grid[z][n]
                cell.is_mine = True

        # Precompute standard Minesweeper clues for non-mine cells
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if getattr(cell, 'is_mine', False):
                    continue
                # Count adjacent mines using 8-neighborhood
                count = 0
                for (nr, nc) in board.get_neighbors(r, c):
                    if board.grid[nr][nc].is_mine:
                        count += 1
                # Store in a generic clue field used by reveal/logic
                cell.clue = count

        # Do not auto-flag or reveal; leave state as hidden to allow solver/policy actions
        return board
