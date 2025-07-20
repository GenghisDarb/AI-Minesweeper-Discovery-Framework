from .board import Board, State
from ai_minesweeper.constants import DEBUG


class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[tuple[int, int], float]:
        """
        Return a rank-ordered false-hypothesis-probability map.

        :param board: The current board state.
        :return: A dictionary mapping cell coordinates to probabilities.
        """
        if DEBUG:
            print("[DEBUG] Board state in RiskAssessor.estimate:")
            for row in board.grid:
                print(" ".join(cell.state.name for cell in row))

        print(f"[RISK] Board rows: {len(board.grid)}")
        for i, row in enumerate(board.grid):
            print(
                f"[RISK] Row {i} length: {len(row)} | Sample: {repr(row[0]) if row else 'EMPTY'}"
            )

        print(
            f"[RISK] Board class: {board.__class__} from module: {board.__class__.__module__}"
        )

        print("[RISK] Calling board.hidden_cells()...")
        result = board.hidden_cells()
        print(f"[RISK] hidden_cells returned {len(result)} cells")

        hidden = board.hidden_cells()
        if DEBUG:
            print(f"[RiskAssessor] Hidden cells found: {len(hidden)}")
            for cell in hidden:
                print(f"Hidden cell: {cell}")
        if not hidden or all(
            cell.is_mine is False and cell.clue is None for row in board.grid for cell in row
        ):
            print("[RISK] No mines or clues found. Returning empty risk map.")
            return {}

        if DEBUG:
            print(
                f"[DEBUG] State.HIDDEN id = {id(State.HIDDEN)} in module risk_assessor"
            )

        base_p = board.false_hypotheses_remaining / len(hidden)
        last_safe = board.last_safe_reveal or (board.n_rows // 2, board.n_cols // 2)

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        probs: dict[tuple[int, int], float] = {}
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board[r, c]
                if cell.is_hidden():
                    adj = board.adjacent_cells(r, c)
                    flagged = sum(1 for v in adj if board.is_flagged(v))
                    hidden_adj = sum(1 for v in adj if board.is_hidden(v))

                    local_risk = (flagged / hidden_adj) if hidden_adj else 0
                    dist_risk = manhattan((r, c), last_safe) / (
                        board.n_rows + board.n_cols
                    )

                    prob = min(
                        0.95,
                        base_p
                        + 1.0 * local_risk  # Increase clue info weight
                        + 0.8 * dist_risk,
                    )  # Increase perimeter exploration weight

                    # Debug: Log intermediate values for risk calculation
                    print(
                        f"Cell: {cell}, Local Risk: {local_risk}, Distance Risk: {dist_risk}, Probability: {prob}"
                    )

                    # Combine randomness with heuristic weights to amplify impact
                    weighted_random_factor = (
                        0.1 * (r + c) / (board.n_rows + board.n_cols)
                    ) * (local_risk + dist_risk)
                    prob += weighted_random_factor

                    # Debug: Log weighted randomness contribution
                    print(
                        f"Cell: {cell}, Weighted Random Factor: {weighted_random_factor}, Probability: {prob}"
                    )

                    # Significantly amplify randomness weight
                    amplified_random_factor = (
                        0.5 * (r + c) / (board.n_rows + board.n_cols)
                    )
                    prob += amplified_random_factor

                    # Debug: Log amplified randomness contribution
                    print(
                        f"Cell: {cell}, Amplified Random Factor: {amplified_random_factor}, Probability: {prob}"
                    )

                    probs[(r, c)] = prob

        # Diagnostic to check if the risk map is flat
        if not any(p < 0.25 for p in probs.values()):
            print("⚠ risk map flat", len(probs), "cells")

        # Temporarily adjust heuristic weights
        local_risk = 0  # Initialize local_risk to avoid UnboundLocalError
        dist_risk = 0  # Initialize dist_risk to avoid UnboundLocalError

        # Ensure probability spectrum is not flat
        if len(set(probs.values())) < len(probs) * 0.5:
            print("⚠ Insufficient probability variance")

        # Debugging output for risk map
        print(f"Risk map: {probs}")

        print(
            f"[RISK] Received board id={id(board)}, class={board.__class__}, grid id={id(board.grid)}"
        )

        return probs

    @staticmethod
    def pick_cell(board: Board) -> tuple[int, int]:
        """
        Select the next cell to probe based on risk assessment.
        """
        for r in range(board.n_rows):
            for c in range(board.n_cols):
                cell = board.grid[r][c]
                if cell.state == State.HIDDEN:
                    return r, c
        return None, None

    def handle_contradiction(self, board, cell):
        """
        Handle a contradiction (mine) without ending the session.

        Args:
            board (Board): The current game board.
            cell (Cell): The cell that caused the contradiction.
        """
        cell.state = State.FLAGGED
        board.update_confidence()  # Update confidence after marking the contradiction
        print(
            f"[INFO] Contradiction at {cell.row}, {cell.col} flagged. Confidence updated."
        )

    @staticmethod
    def choose_move(board: Board) -> tuple[int, int]:
        """
        Choose the next move based on the lowest probability.

        :param board: The current board state.
        :return: Coordinates (row, col) of the chosen move.
        """
        probabilities = RiskAssessor.estimate(board)
        if not probabilities:
            raise RuntimeError("No valid moves remaining.")

<<<<<<< HEAD
        # Find the cell with the lowest probability
        move = min(probabilities, key=probabilities.get)
        return move
=======
        if not prob_map:
            return None

        # Extract safest cell (lowest probability)
        best_coord = min(prob_map, key=prob_map.get)
        row, col = best_coord
        cell = board.grid[row][col]

        if cell.state.value == State.HIDDEN.value:
            # Set row/col attributes for the cell if not already set
            if cell.row is None:
                cell.row = row
            if cell.col is None:
                cell.col = col
            return cell  # Return Cell object instead of coordinates
        return None
>>>>>>> origin/copilot/fix-73693070-4d50-40b0-97b0-72eeb69256fe
