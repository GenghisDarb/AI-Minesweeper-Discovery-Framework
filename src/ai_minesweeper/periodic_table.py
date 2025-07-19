class PeriodicTableDomain:
    @staticmethod
    def is_mine(cell):
        print(
            f"[DEBUG] Checking if cell is mine: state={cell.state}, symbol={cell.symbol}"
        )  # Debugging output
        mine_symbols = {
            "li",
            "be",
            "b",
            "f",
            "cl",
            "br",
            "i",
            "eka",
            "x",  # Added X to mine symbols
        }
        return cell.symbol.lower() in mine_symbols

    @staticmethod
    def get_neighbors(cell, board):
        neighbors = []
        for other in board.cells:
            if (
                other.group == cell.group or other.period == cell.period
            ) and other != cell:
                neighbors.append(other)
        # Ensure unique neighbors and correct count
        unique_neighbors = []
        for neighbor in neighbors:
            if neighbor not in unique_neighbors:
                unique_neighbors.append(neighbor)
        return unique_neighbors

    @staticmethod
    def generate_clue(cell, neighbors):
        print(f"Generating clue for cell: symbol={cell.symbol}")  # Debugging output
        return sum(1 for neighbor in neighbors if PeriodicTableDomain.is_mine(neighbor))
