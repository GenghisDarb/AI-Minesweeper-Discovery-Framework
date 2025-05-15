# from collections import defaultdict   # ← remove if not needed
from dataclasses import dataclass

@dataclass(frozen=True)
class Cluster:
    hidden: frozenset[tuple[int, int]]
    constraints: tuple

def collect_constraints(board) -> list:
    constraints = []
    for r, row in enumerate(board.grid):
        for c, cell in enumerate(row):
            if cell.state.name == "REVEALED" and getattr(cell, "clue", 0) > 0:
                hidden = []
                flagged = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if hasattr(board, "in_bounds") and board.in_bounds(nr, nc):
                            ncell = board.grid[nr][nc]
                            if ncell.state.name == "HIDDEN":
                                hidden.append((nr, nc))
                            elif ncell.state.name == "FLAGGED":
                                flagged += 1
                if hidden:
                    # Import Constraint here to avoid circular import
                    from .constraints import Constraint
                    constraints.append(Constraint((r, c), tuple(hidden), getattr(cell, "clue", 0) - flagged))
    return constraints

def split_clusters(constraints):
    """Group constraints whose hidden-cell sets overlap."""
    clusters = []
    processed = set()

    for con in constraints:
        if con in processed:
            continue
        cluster_cons = {con}
        cluster_hidden = set(con.hidden)

        changed = True
        while changed:
            changed = False
            for other in constraints:
                if other in cluster_cons:
                    continue
                if cluster_hidden & set(other.hidden):
                    cluster_cons.add(other)
                    cluster_hidden |= set(other.hidden)
                    changed = True

        clusters.append(
            Cluster(hidden=tuple(cluster_hidden), constraints=tuple(cluster_cons))
        )
        processed |= cluster_cons

    return clusters

def combine(cluster_maps):
    """Combine probability maps from clusters into a unified map."""
    probs = {}
    for sub in cluster_maps:
        probs.update(sub)
    return probs

def enumerate_cluster(cluster) -> dict[tuple[int, int], float]:
    """Exact enumeration for small clusters."""
    cells = list(cluster.hidden)
    n = len(cells)
    freq = [0] * n
    total = 0
    # Only enumerate if n is small (e.g., ≤15)
    if n > 15:
        raise ValueError("Cluster too large for exact enumeration")
    for mask in range(1 << n):
        assign = {cells[i]: bool(mask & (1 << i)) for i, cell in enumerate(cells)}
        if all(sum(assign[c] for c in con.hidden) == con.mines for con in cluster.constraints):
            total += 1
            for i, cell in enumerate(cells):
                if assign[cell]:
                    freq[i] += 1
    if total == 0:
        return {cell: 0.0 for cell in cells}
    return {cell: freq[i] / total for i, cell in enumerate(cells)}
