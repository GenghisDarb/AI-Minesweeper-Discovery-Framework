import unittest
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.click_engine import ClickEngine
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.state import State

class TestRiskEngine(unittest.TestCase):
    def test_lowest_risk_chosen(self):
        board = BoardBuilder.from_csv('examples/boards/mini.csv')
        r, c = ClickEngine.next_click(board)
        self.assertNotEqual(board.grid[r][c].is_mine, True, "Selected cell should not be a mine")

    def test_risk_zero_with_zero_adjacent(self):
        # Create a 3x3 board with no mines
        board = Board(3, 3)
        # Manually reveal (0,0) and set its adjacent mine count to 0
        board.grid[0][0].state = State.REVEALED
        board.grid[0][0].adjacent_mines = 0
        # Estimate risks
        risks = RiskAssessor.estimate(board)
        # Assert that all hidden cells have a risk of 0.0
        for r in range(3):
            for c in range(3):
                if board.grid[r][c].state == State.HIDDEN:
                    self.assertEqual(risks[(r, c)], 0.0, f"Risk for cell ({r},{c}) should be 0.0")

if __name__ == '__main__':
    unittest.main()
