import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from ai_minesweeper.ui_widgets import display_confidence


def test_display_confidence_cli():
    conf = 0.75
    output = display_confidence(conf, mode="cli")
    assert "Confidence: 75.0%" in output
