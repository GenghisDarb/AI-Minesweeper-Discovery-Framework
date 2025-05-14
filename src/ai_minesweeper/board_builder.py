class BoardBuilder:
from .board import Board

    """Ingests domain relations & builds cell network."""
    def __init__(self, relations):
        self.relations = relations

    def build(self):
        # TODO: Implement cell network construction
        pass

    @staticmethod
    def from_csv(path) -> Board:
        with open(path, 'r') as file:
            lines = file.readlines()

        n_rows = len(lines)
        n_cols = len(lines[0].strip().split(','))

        board = Board(n_rows, n_cols)

        for row_index, line in enumerate(lines):
            cells = line.strip().split(',')
            for col_index, cell in enumerate(cells):
                if cell == '*':
                    board.grid[row_index][col_index].is_mine = True
                else:
                    board.grid[row_index][col_index].is_mine = False

        board.compute_adjacent_mines()
        return board
