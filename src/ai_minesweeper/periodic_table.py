from ai_minesweeper.board import State


class PeriodicTableDomain:
    @staticmethod
    def is_mine(cell):
        print(
            f"[DEBUG] Checking if cell is mine: state={cell.state}, symbol={cell.symbol}"
        )
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
        return (
            cell.symbol
            and cell.symbol.lower() in mine_symbols
            and cell.state == State.HIDDEN
        )

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
        print(f"Generating clue for cell: symbol={cell.symbol}")
        return sum(1 for neighbor in neighbors if PeriodicTableDomain.is_mine(neighbor))
