from ai_minesweeper import BoardBuilder
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
from ai_minesweeper.risk_assessor import SpreadRiskAssessor

## Quick test for basic workflow


def test_quick():
    # Example grid: 3x3 with a mine and some clues
    grid = [["M", "", ""], ["", 1, ""], ["", "", "M"]]

    # Build the board
    board = BoardBuilder.from_manual(grid)
    assessor = SpreadRiskAssessor()

    # Initialize ConfidencePolicy with proper instantiation
    confidence = BetaConfidence()
    policy = ConfidencePolicy(SpreadRiskAssessor(), confidence)

    # Simulate one step
    probs = assessor.get_probabilities(board)
    assert probs is not None, "Probabilities should not be None"

    choice = policy.choose_move(board)
    assert choice is not None, "Policy should choose a move"
    # Accept tuple or Cell
    if hasattr(choice, 'row') and hasattr(choice, 'col'):
        print("Chosen hypothesis to test:", (choice.row, choice.col))
    else:
        print("Chosen hypothesis to test:", choice)
    print("Initial probabilities:", probs)
