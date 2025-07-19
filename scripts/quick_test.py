from ai_minesweeper import BoardBuilder
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "tests"))
from helpers.risk_assessor_spread import SpreadRiskAssessor
import argparse

# Define a trivial domain: 3 hypotheses, with a simple constraint like "at most 1 of these 3 is false".
# hypotheses = [
#     {"id": 1, "desc": "Hypothesis A", "neighbors": [2, 3]},
#     {"id": 2, "desc": "Hypothesis B", "neighbors": [1, 3]},
#     {"id": 3, "desc": "Hypothesis C", "neighbors": [1, 2]}
# ]
# constraints = [
#     {"neighbors": [1, 2, 3], "max_false": 1}
# ]

# Replace hypotheses and constraints with a valid 2D grid
# Example grid: 3x3 with a mine and some clues
grid = [["M", "", ""], ["", 1, ""], ["", "", "M"]]

# Build the board
board = BoardBuilder.from_manual(grid)
assessor = SpreadRiskAssessor()

# Parse CLI arguments
parser = argparse.ArgumentParser(
    description="Run Minesweeper with optional Meta-Cell Confidence Module."
)
parser.add_argument(
    "--use-confidence", action="store_true", help="Enable Meta-Cell Confidence Module"
)
parser.add_argument(
    "-q", "--quiet", action="store_true", help="Run in quiet mode (minimal output)"
)
args = parser.parse_args()

# Initialize ConfidencePolicy conditionally
if args.use_confidence:
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor, confidence)
    print("Meta-Cell Confidence Module enabled.")
else:
    policy = SpreadRiskAssessor
    print("Meta-Cell Confidence Module disabled.")

# Simulate one step
probs = assessor.get_probabilities(board)
print("Initial probabilities:", probs)
choice = policy.choose_move(board)
print("Chosen hypothesis to test:", choice)

for cell, prob in probs.items():
    r, c = cell.row, cell.col
    if cell.is_hidden():
        # ...existing logic...
        pass
