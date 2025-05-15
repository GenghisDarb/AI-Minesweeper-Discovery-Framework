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
        constraints = collect_constraints(board)
        clusters = split_clusters(constraints)

        probabilities = {}
        for cluster in clusters:
            if len(cluster.hidden) <= MAX_ENUM:
                cluster_probs = enumerate_cluster(cluster)
            else:
                cluster_probs = mc_cluster(cluster)
            probabilities.update(cluster_probs)

        return probabilities
