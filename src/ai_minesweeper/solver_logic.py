from .board import Board, State


class Flagger:
    @staticmethod
    def mark_contradictions(board: Board) -> bool:
        """
        Flag cells as potentially false hypotheses based on logical deduction.
        """
        flagged = False
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.state == State.REVEALED and cell.adjacent_mines > 0:
                    hidden_neighbors = [
                        nbr
                        for nbr in board.neighbors(r, c)
                        if nbr.state == State.HIDDEN
                    ]
                    if (
                        len(hidden_neighbors) == cell.adjacent_mines
                    ):  # Adjusted to inferred risk
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
                    flagged_neighbors = [
                        nbr
                        for nbr in board.neighbors(r, c)
                        if nbr.state == State.FLAGGED
                    ]
                    if len(flagged_neighbors) == cell.adjacent_mines:
                        hidden_neighbors = [
                            nbr
                            for nbr in board.neighbors(r, c)
                            if nbr.state == State.HIDDEN
                        ]
                        for nbr in hidden_neighbors:
                            board.reveal(nbr.row, nbr.col, flood=True)
                            revealed = True
        return revealed


class SolverLogic:
    @staticmethod
    def flag_mines(board):
        changed = False
        for cell in board.revealed_cells():
            clue = board.clue(cell)
            adj = board.adjacent_cells(
                cell.row, cell.col
            )  # Pass row and col explicitly
            hidden = [c for c in adj if board.is_hidden(c)]
            flagged = [c for c in adj if board.is_flagged(c)]

            if clue is None:
                continue

            if clue - len(flagged) == len(hidden):
                for c in hidden:
                    board.flag(c)
                    print(f"Flagged cell {c} based on clue {clue}")  # Debugging output
                    changed = True
        return changed

    @staticmethod
    def cascade_reveal(board):
        changed = False
        queue = list(board.revealed_cells())

        visited = set(queue)

        while queue:
            cell = queue.pop(0)
            clue = board.clue(cell)
            adj = board.adjacent_cells(cell.row, cell.col)
            hidden = [c for c in adj if board.is_hidden(c)]

            # Debugging output for cascade reveal
            print(f"Queue: {queue}")
            print(f"Visited: {visited}")
            print(f"Hidden cells: {hidden}")

            if clue is None or len(hidden) == 0:
                continue

            if clue == len(hidden):
                for c in hidden:
                    board.reveal(c[0], c[1], flood=True)
                    print(f"Revealed cell {c} based on clue {clue}")  # Debugging output
                    changed = True
                    if c not in visited:
                        queue.append(c)
                        visited.add(c)
            elif clue == 0:
                for c in hidden:
                    board.reveal(c[0], c[1], flood=True)
                    print(f"Revealed cell {c} based on clue {clue}")  # Debugging output
                    changed = True
                    if c not in visited:
                        queue.append(c)
                        visited.add(c)
            else:
                if not cell.state.is_hidden():
                    continue
                cell.reveal()
                if cell.clue == 0:
                    queue.extend(
                        n for n in cell.neighbors() if n.state.is_hidden()
                    )  # Ensure only hidden neighbors are appended
        return changed
