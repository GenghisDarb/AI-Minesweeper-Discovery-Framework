from ai_minesweeper.board import Board
from ai_minesweeper.prob import (
    collect_constraints,
    split_clusters,
    enumerate_cluster,
    mc_cluster,
)

MAX_ENUM = 15  # brute-force cutoff


class RiskAssessor:
    """OO façade around the hybrid probability engine."""

    def __init__(self, board: Board) -> None:
        self.board = board

    # ---- public API -----------------------------------------------------
    def compute_probabilities(self) -> dict[tuple[int, int], float]:
        cons = collect_constraints(self.board)
        if not cons:
            # opening move → uniform risk
            n = self.board.n_rows * self.board.n_cols
            return {(r, c): 1 / n
                    for r in range(self.board.n_rows)
                    for c in range(self.board.n_cols)}

        clusters = split_clusters(cons)
        probs: dict[tuple[int, int], float] = {}
        for cl in clusters:
            sub = (enumerate_cluster(cl)
                   if len(cl.hidden) <= MAX_ENUM
                   else mc_cluster(cl))
            probs.update(sub)
        return probs

    def choose_move(self) -> tuple[int, int]:
        """Return the hidden cell with minimum mine probability."""
        probs = self.compute_probabilities()
        return min(probs.items(), key=lambda kv: kv[1])[0]

    # single method covers both usages:
    #   • RiskAssessor.estimate(board)          ← static-style
    #   • RiskAssessor(board).estimate()        ← instance-style
    def estimate(self_or_board) -> dict[tuple[int, int], float]:
        """
        If called as RiskAssessor.estimate(board): self_or_board is a Board.
        If called as instance.estimate():          self_or_board is a RiskAssessor.
        """
        from ai_minesweeper.board import Board  # local to avoid cycle

        if isinstance(self_or_board, Board):
            board_obj = self_or_board                         # static style
        else:
            board_obj = self_or_board.board                   # instance style

        return RiskAssessor(board_obj).compute_probabilities()


__all__ = ["RiskAssessor"]
