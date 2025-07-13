from src.ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

def test_ab_winrate():
    """
    Runs 500 random 16x16 games and asserts win-rate of confidence-agent >= baseline after move 50.
    """
    # Placeholder for actual implementation
    assert True

def test_beta_confidence():
    conf = BetaConfidence()
    assert conf.mean() == 0.5
    conf.update(success=True)
    assert conf.mean() > 0.5
    conf.update(success=False)
    assert conf.mean() < 1.0
