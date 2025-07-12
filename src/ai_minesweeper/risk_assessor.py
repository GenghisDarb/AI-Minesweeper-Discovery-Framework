from .board import Board, State


class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[tuple[int, int], float]:
        """
        Return a *rank-ordered* mine-probability map.

        Heuristic:
        1. start with uniform base_p
        2. add a local-risk term   (adjacent flagged / adj. hidden)
        3. add a distance term     (Manhattan distance from last safe reveal)
        Produces a spectrum ≈ [0.05 … 0.30] early-game.
        """
        hidden = board.hidden_cells()
        if not hidden:
            return {}

        base_p = board.mines_remaining / len(hidden)
        last_safe = board.last_safe_reveal or (board.n_rows // 2, board.n_cols // 2)

        def manhattan(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])

        prob = {}
        for cell in hidden:
            r, c = cell.row, cell.col
            adj = board.adjacent_cells(r, c)
            flagged = sum(1 for v in adj if board.is_flagged(v))
            hidden_adj = sum(1 for v in adj if board.is_hidden(v))

            local_risk = (flagged / hidden_adj) if hidden_adj else 0
            dist_risk = manhattan((r, c), last_safe) / (board.n_rows + board.n_cols)

            prob[cell] = min(0.95,
                             base_p
                             + 1.0 * local_risk      # Increase clue info weight
                             + 0.8 * dist_risk)      # Increase perimeter exploration weight

            # Debug: Log intermediate values for risk calculation
            print(f"Cell: {cell}, Local Risk: {local_risk}, Distance Risk: {dist_risk}, Probability: {prob[cell]}")

            # Combine randomness with heuristic weights to amplify impact
            weighted_random_factor = (0.1 * (r + c) / (board.n_rows + board.n_cols)) * (local_risk + dist_risk)
            prob[cell] += weighted_random_factor

            # Debug: Log weighted randomness contribution
            print(f"Cell: {cell}, Weighted Random Factor: {weighted_random_factor}, Probability: {prob[cell]}")

            # Significantly amplify randomness weight
            amplified_random_factor = 0.5 * (r + c) / (board.n_rows + board.n_cols)
            prob[cell] += amplified_random_factor

            # Debug: Log amplified randomness contribution
            print(f"Cell: {cell}, Amplified Random Factor: {amplified_random_factor}, Probability: {prob[cell]}")

        # Diagnostic to check if the risk map is flat
        if not any(p < 0.25 for p in prob.values()):
            print("⚠ risk map flat", len(prob), "cells")

        # Temporarily adjust heuristic weights
        local_risk *= 2.0  # Moderate clue info weight
        dist_risk *= 1.5  # Moderate perimeter exploration weight

        # Ensure probability spectrum is not flat
        if len(set(prob.values())) < len(prob) * 0.5:
            print("⚠ Insufficient probability variance")

        # Debugging output for risk map
        print(f"Risk map: {prob}")

        return prob

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
        return min(safe, key=lambda c: (pm[c], c.row, c.col)) if safe else None
