from .board import Board, State

class RiskAssessor:
    """Very naïve probability map."""

    @staticmethod
        @staticmethod
    def estimate(board) -> dict[tuple[int, int], float]:
        risk_map: dict[tuple[int, int], float] = {}
        for r, row in enumerate(board.grid):
            for c, cell in enumerate(row):
                if cell.state == State.HIDDEN:
                    # Check revealed neighbors
                    revealed_neighbors = [board.grid[nr][nc] for nr, nc in board.get_neighbors(r, c) if board.grid[nr][nc].state == State.REVEALED]
                    if any(neighbor.adjacent_mines == 0 for neighbor in revealed_neighbors):
                        risk_map[(r, c)] = 0.0
                    else:
                        # Calculate risk based on revealed neighbors
                        sum_neighbor_counts = sum(neighbor.adjacent_mines for neighbor in revealed_neighbors)
                        num_hidden_neighbors = len([1 for nr, nc in board.get_neighbors(r, c) if board.grid[nr][nc].state == State.HIDDEN])
                        if num_hidden_neighbors > 0:
                            risk_map[(r, c)] = sum_neighbor_counts / (num_hidden_neighbors * 8)
                        else:
                            risk_map[(r, c)] = 1.0
                elif cell.is_mine:
                    risk_map[(r, c)] = 1.0
                else:
                    risk_map[(r, c)] = 0.0
        return risk_map
