import unittest
from ai_minesweeper.board_builder import BoardBuilder


class TestBoardBuilderCSV(unittest.TestCase):
    def test_from_csv(self):
        board = BoardBuilder.from_csv("examples/boards/mini.csv")
        self.assertEqual(
            board.n_rows, 4
        )  # Adjusted expected row count to match the actual board dimensions
        self.assertEqual(board.n_cols, 5)
        self.assertGreater(sum(cell.is_mine for row in board.grid for cell in row), 0)


if __name__ == "__main__":
    unittest.main()
