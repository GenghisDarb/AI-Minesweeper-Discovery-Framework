import unittest

from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.click_engine import ClickEngine


class TestClickEngine(unittest.TestCase):
    def test_next_click_within_bounds(self):
        board = BoardBuilder.from_csv("examples/boards/mini.csv")
        r, c = ClickEngine.next_click(board)
        self.assertTrue(0 <= r < board.n_rows)
        self.assertTrue(0 <= c < board.n_cols)


if __name__ == "__main__":
    unittest.main()
