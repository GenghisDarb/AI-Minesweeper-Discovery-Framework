# from collections import defaultdict   # ← remove if not needed
from dataclasses import dataclass

@dataclass(frozen=True)
class Cluster:
    hidden: frozenset[tuple[int, int]]
    constraints: tuple

def collect_constraints(board) -> list[Constraint]:
    constraints = []
    for r, row in enumerate(board.grid):
        for c, cell in enumerate(row):
            if cell.state is State.REVEALED and cell.clue > 0:
                hidden = []
                flagged = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if not board.in_bounds(nr, nc):
                            continue
                        ncell = board.grid[nr][nc]
                        if ncell.state is State.HIDDEN:
                            hidden.append((nr, nc))
                        elif getattr(ncell, "is_mine", False):
                            flagged += 1
                # ✱ Only create a constraint if there is **at least one** hidden neighbour
                if hidden:
                    constraints.append(
                        Constraint((r, c), tuple(hidden), cell.clue - flagged)
                    )
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
