from .board import Board, State

class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
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
