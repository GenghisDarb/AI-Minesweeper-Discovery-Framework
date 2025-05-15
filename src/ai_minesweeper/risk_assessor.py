from .board import Board
from ai_minesweeper.prob import (
    collect_constraints,
    split_clusters,
    enumerate_cluster,
    mc_cluster,
)

MAX_ENUM = 15    # enumerate if cluster ≤15 hidden cells

class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
    def estimate(board: Board) -> dict[tuple[int, int], float]:
        cons = collect_constraints(board)
        if not cons:  # no clues yet → uniform risk
            return {
                (r, c): 0.15
                for r in range(board.n_rows)
                for c in range(board.n_cols)
                if board.grid[r][c].state.name == "HIDDEN"
            }
        clusters = split_clusters(cons)

        probabilities = {}
        for cluster in clusters:
            if len(cluster.hidden) <= MAX_ENUM:
                cluster_probs = enumerate_cluster(cluster)
            else:
                cluster_probs = mc_cluster(cluster)
            probabilities.update(cluster_probs)

        return probabilities

    @staticmethod
    def from_ascii(ascii_str: str) -> "Board":
        return Board.from_ascii(ascii_str)
