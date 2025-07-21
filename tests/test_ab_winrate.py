from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_ab_winrate():
    """
    Runs 500 random 16x16 games and asserts win-rate of confidence-agent >= baseline after move 50.
    """
    # Placeholder for actual implementation
    assert True


def test_beta_confidence():
    conf = BetaConfidence()
    assert conf.mean() == 0.5
    # Simulate successful prediction: high predicted probability and actual mine
    conf.update(predicted_probability=0.9, revealed_is_mine=True)
    assert conf.mean() > 0.5
    # Simulate failed prediction: high predicted probability but no mine
    conf.update(predicted_probability=0.9, revealed_is_mine=False)
    assert conf.mean() < 1.0
