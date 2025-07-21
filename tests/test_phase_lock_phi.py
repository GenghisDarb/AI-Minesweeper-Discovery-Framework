"""
Unit tests for Phase-Lock Minesweeper Module
"""

import unittest

import numpy as np

from ai_minesweeper.domain.phase_lock_phi import detect_phi_reset


class TestPhaseLockPhi(unittest.TestCase):
    def test_phi_reset_detection(self):
        """
        Validate detection on synthetic reset signal.
        """
        sampling_rate = 1000
        signal = np.sin(2 * np.pi * 13 * np.arange(0, 1, 1 / sampling_rate))
        signal[700:800] += np.sin(2 * np.pi * 13 * np.arange(0, 0.1, 1 / sampling_rate))
        reset_detected = detect_phi_reset(signal, sampling_rate)
        self.assertTrue(reset_detected)


if __name__ == "__main__":
    unittest.main()
