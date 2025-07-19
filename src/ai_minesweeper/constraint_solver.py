# src/ai_minesweeper/constraint_solver.py
from ai_minesweeper.cell import State


class ConstraintSolver:
    def choose_move(self, board):
        """
        Choose the next move based on deterministic Minesweeper rules.

        :param board: The current board state.
        :return: A tuple (row, col) for the next move, or None if no move is possible.
        """
        for row in board.grid:
            for cell in row:
                if cell.state == State.REVEALED and cell.clue is not None:
                    neighbors = board.get_neighbors(cell)
                    hidden_neighbors = [n for n in neighbors if n.state == State.HIDDEN]
                    flagged_neighbors = [n for n in neighbors if n.state == State.FLAGGED]

                    # Rule 1: If clue equals the number of hidden neighbors, flag all hidden neighbors
                    if len(hidden_neighbors) == cell.clue:
                        for neighbor in hidden_neighbors:
                            neighbor.state = State.FLAGGED
                        return None  # Continue solving

                    # Rule 2: If clue equals the number of flagged neighbors, reveal all other hidden neighbors
                    if len(flagged_neighbors) == cell.clue:
                        for neighbor in hidden_neighbors:
                            neighbor.state = State.REVEALED
                        return None  # Continue solving

        # Fallback: No deterministic move found
        return None

    def solve(self, board):
        # Delegate to core logic
        return self.choose_move(board)
