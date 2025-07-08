

class PeriodicTableDomain:
    @staticmethod
    def get_neighbors(cell, board):
        neighbors = []
        for other in board.cells:
            if other.group == cell.group or other.period == cell.period:
                neighbors.append(other)
        return neighbors

    @staticmethod
    def is_mine(cell):
        return cell.symbol.startswith("eka")  # Example logic for unfilled positions

    @staticmethod
    def generate_clue(cell, neighbors):
        return sum(1 for neighbor in neighbors if PeriodicTableDomain.is_mine(neighbor))
