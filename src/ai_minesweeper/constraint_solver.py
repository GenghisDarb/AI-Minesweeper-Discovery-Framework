from ai_minesweeper.board import State
from ai_minesweeper.risk_assessor import RiskAssessor


class ConstraintSolver:
    def __init__(self):
        self.risk_assessor = RiskAssessor()

    def choose_move(self, board):
        """
        Choose the next move based on deterministic Minesweeper rules.

        :param board: The current board state.
        :return: A Cell object for the next move, or None if no move is possible.
        """
        for row in board.grid:
            for cell in row:
                if cell.state == State.REVEALED and cell.clue is not None:
                    neighbors = board.neighbors(cell.row, cell.col)
                    hidden_neighbors = [n for n in neighbors if n.state == State.HIDDEN]
                    flagged_neighbors = [
                        n for n in neighbors if n.state == State.FLAGGED
                    ]

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

        # Fallback: Use RiskAssessor for probabilistic move
        return self.risk_assessor.choose_move(board)

    def solve(self, board):
        """
        Solve the board by applying moves until no more moves are possible.
        """
        moves = 0
        max_moves = 100
        while moves < max_moves:
            move = self.choose_move(board)
            if move is None:
                break
            board.reveal(move.row, move.col)
            moves += 1
