import random

def mc_cluster(cluster, iterations=1000):
    hidden_cells = cluster.hidden
    constraints = cluster.constraints
    counts = {cell: 0 for cell in hidden_cells}

    for _ in range(iterations):
        # Generate a random configuration
        configuration = {cell: random.choice([0, 1]) for cell in hidden_cells}
        
        # Check if the configuration satisfies all constraints
        if all(sum(configuration[cell] for cell in con.hidden) == con.mines for con in constraints):
            for cell in hidden_cells:
                counts[cell] += configuration[cell]

    # Calculate probabilities
    total_valid = sum(counts.values())
    if total_valid == 0:
        return {cell: 1/len(hidden_cells) for cell in hidden_cells}  # fallback to uniform probability
    return {cell: counts[cell] / total_valid for cell in hidden_cells}
