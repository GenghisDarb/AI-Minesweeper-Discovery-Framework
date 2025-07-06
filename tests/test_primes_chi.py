"""
Unit tests for Prime Residue Minesweeper Module
"""

import unittest
from ai_minesweeper.domain.primes_chi import (
    build_board,
    evaluate_cell,
    compute_ridge_score,
)


class TestPrimesChi(unittest.TestCase):
    def test_ridge_score(self):
        """
        Test that ridge score S > 2 for a small prime window.
        """
        board = build_board(10, 100)
        ridge_score = compute_ridge_score()
        self.assertGreater(ridge_score, 2)


if __name__ == "__main__":
    unittest.main()
