from .board import Board, State

class Flagger:
    @staticmethod
    def mark_contradictions(board: Board) -> bool:
        """
        Flag cells as mines based on logical deduction.
        """
        flagged = False
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.state == State.REVEALED and cell.adjacent_mines > 0:
                    hidden_neighbors = [nbr for nbr in board.neighbors(r, c) if nbr.state == State.HIDDEN]
                    if len(hidden_neighbors) == cell.adjacent_mines:
                        for nbr in hidden_neighbors:
                            board.flag(nbr.row, nbr.col)
                            flagged = True
        return flagged

class CascadePropagator:
    @staticmethod
    def open_safe_neighbors(board: Board) -> bool:
        """
        Reveal safe cells based on logical deduction.
        """
        revealed = False
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.state == State.REVEALED and cell.adjacent_mines > 0:
                    flagged_neighbors = [nbr for nbr in board.neighbors(r, c) if nbr.state == State.FLAGGED]
                    if len(flagged_neighbors) == cell.adjacent_mines:
                        hidden_neighbors = [nbr for nbr in board.neighbors(r, c) if nbr.state == State.HIDDEN]
                        for nbr in hidden_neighbors:
                            board.reveal(nbr.row, nbr.col, flood=True)
                            revealed = True
        return revealed
