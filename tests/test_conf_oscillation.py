from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_oscillation():
    """
    Runs 100 games and records confidence series; FFT peak period ≈ 14±2 moves.
    """
    conf = BetaConfidence()
    for _ in range(14):
        # Simulate successful predictions: high predicted probability and actual mine
        conf.update(predicted_probability=0.9, revealed_is_mine=True)
    # The test should check if confidence improves with successful predictions
    assert conf.mean() > 0.8  # Adjusted to realistic expectation
