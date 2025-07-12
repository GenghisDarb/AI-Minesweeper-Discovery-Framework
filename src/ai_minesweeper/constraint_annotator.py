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
                if cell.is_false_hypothesis:
                    cell.adjacent_false_hypotheses = (
                        -1
                    )  # Convention: -1 for false hypotheses
                else:
                    neighbors = board.neighbors(r, c)
                    cell.adjacent_false_hypotheses = sum(
                        1 for nbr in neighbors if nbr.is_false_hypothesis
                    )
