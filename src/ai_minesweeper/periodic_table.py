

class PeriodicTableDomain:
    @staticmethod
    def is_mine(cell):
        """Return True if the cell represents a mine by periodic-table semantics.

        Count mines by symbol regardless of current state so that explicitly-flagged
        mines (e.g., 'X' from CSV on small demo boards) are recognized by the domain.
        """
        mine_symbols = {
            "li",
            "be",
            "b",
            "f",
            "cl",
            "br",
            "i",
            "eka",
            "x",
            "mine",
        }
        return bool(getattr(cell, "symbol", None)) and str(cell.symbol).lower() in mine_symbols

    @staticmethod
    def get_neighbors(cell, board):
        if not board.grid:
            return []
        neighbors = []
        for row in board.grid:
            for other in row:
                if (
                    other.group == cell.group or other.period == cell.period
                ) and other != cell:
                    neighbors.append(other)
        unique_neighbors = list({neighbor: None for neighbor in neighbors})
        return unique_neighbors

    @staticmethod
    def generate_clue(cell, neighbors):
        return sum(1 for neighbor in neighbors if PeriodicTableDomain.is_mine(neighbor))
