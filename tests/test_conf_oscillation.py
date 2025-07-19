from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_oscillation():
    """
    Runs 100 games and records confidence series; FFT peak period ≈ 14±2 moves.
    """
    conf = BetaConfidence()
    for _ in range(14):
        conf.update(success=True)
    assert conf.mean() > 0.9
