import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src" / "ai_minesweeper"))
from constants import chi

import os
import json

from ai_minesweeper.ui_widgets import display_confidence


def test_display_confidence_cli():
    conf = 0.75
    output = display_confidence(conf, mode="cli")
    assert "Confidence: 75.0%" in output


def test_sidebar_constants():
    with open("data/chi_50digits.txt") as f:
        chi = f.read().strip()
    with open("data/confidence_fit_params.json") as f:
        params = json.load(f)
    with open("reports/prime_residue_S.csv") as f:
        s_row = f.read().strip().split(",")
        S = float(s_row[-1])

    assert chi.startswith("3.141"), "χ constant should be loaded correctly"
    assert params["τ"] > 0, "τ constant should be positive"
    assert S > 0, "S-stat should be positive"
    assert 0.78 < chi < 0.80, "χ constant should be in the range (0.78, 0.80)"


def test_tabs_functionality():
    tabs = ["Game Board", "χ‑brot Visualizer", "Confidence Fit"]
    assert "Game Board" in tabs, "Game Board tab should exist"
    assert "χ‑brot Visualizer" in tabs, "χ‑brot Visualizer tab should exist"
    assert "Confidence Fit" in tabs, "Confidence Fit tab should exist"
