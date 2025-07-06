from .board import Board


class ConstraintAnnotator:
    @staticmethod
    def annotate(board: Board) -> None:
        """
        Assign clue numbers to each cell based on its neighbors.
        """
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell is None:
                    continue  # Skip unused cells
                if cell.is_mine:
                    cell.adjacent_mines = -1  # Convention: -1 for mines
                else:
                    neighbors = board.neighbors(r, c)
                    cell.adjacent_mines = sum(1 for nbr in neighbors if nbr.is_mine)
