from collections import defaultdict
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

def split_clusters(constraints: list) -> list[Cluster]:
    """Group constraints into clusters if their hidden sets overlap."""
    parent = {}
    sets = [set(con.hidden) for con in constraints]

    # Union-find helpers
    def find(i):
        while parent.get(i, i) != i:
            i = parent[i]
        return i

    def union(i, j):
        pi, pj = find(i), find(j)
        if pi != pj:
            parent[pi] = pj

    # Union constraints with overlapping hidden sets
    for i, si in enumerate(sets):
        for j in range(i + 1, len(sets)):
            sj = sets[j]
            if si & sj:
                union(i, j)

    # Group by root
    clusters = defaultdict(list)
    for idx, con in enumerate(constraints):
        clusters[find(idx)].append(con)

    # Build Cluster objects
    result = []
    for group in clusters.values():
        all_hidden = set()
        for con in group:
            all_hidden.update(con.hidden)
        result.append(Cluster(frozenset(all_hidden), tuple(group)))
    return result

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
        assign = {cells[i]: bool(mask & (1 << i)) for i in range(n)}
        if all(sum(assign[c] for c in con.hidden) == con.mines for con in cluster.constraints):
            total += 1
            for i, cell in enumerate(cells):
                if assign[cell]:
                    freq[i] += 1
    if total == 0:
        # No valid assignments, assign uniform zero
        return {cell: 0.0 for cell in cells}
    return {cell: freq[i] / total for i, cell in enumerate(cells)}