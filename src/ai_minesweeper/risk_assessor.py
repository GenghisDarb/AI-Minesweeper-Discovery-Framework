from .board import Board, State


class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[tuple[int, int], float]:
        """
        Return a *rank-ordered* false-hypothesis-probability map.

        Heuristic:
        1. start with uniform base_p
        2. add a local-risk term   (adjacent flagged / adj. hidden)
        3. add a distance term     (Manhattan distance from last safe reveal)
        Produces a spectrum ≈ [0.05 … 0.30] early-game.
        """
        print("[DEBUG] Board state in RiskAssessor.estimate:")
        for row in board.grid:
            print(" ".join(cell.state.name for cell in row))

        hidden = board.hidden_cells()
        print(f"[RiskAssessor] Hidden cells found: {len(hidden)}")
        for cell in hidden:
            print(f"Hidden cell: {cell}")
        if not hidden:
            return {}

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
        local_risk *= 2.0  # Moderate clue info weight
        dist_risk *= 1.5  # Moderate perimeter exploration weight

        # Ensure probability spectrum is not flat
        if len(set(probs.values())) < len(probs) * 0.5:
            print("⚠ Insufficient probability variance")

        # Debugging output for risk map
        print(f"Risk map: {probs}")

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

    @staticmethod
    def choose_move(board: Board):
        """
        Return the Cell with the **lowest** mine‐probability.
        If multiple cells tie, choose the one with minimal (row,col).
        """
        pm = RiskAssessor.estimate(board)
        safe = [c for c in pm if c.state == State.HIDDEN]
        move = min(safe, key=lambda c: (pm[c], c.row, c.col)) if safe else None

        # Debugging output for the chosen move
        print(f"Chosen move: {move}, Probability: {pm[move] if move else 'N/A'}")
        print(f"Probability map: {pm}")
        print(f"Safe cells: {safe}")

        return move
