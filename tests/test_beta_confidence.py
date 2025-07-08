import pytest
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_update():
    conf = BetaConfidence()
    conf.update(0.5, True)  # Predicted 50% mine, revealed as mine
    assert conf.alpha == 1.5
    assert conf.beta == 1.0

    conf.update(0.5, False)  # Predicted 50% mine, revealed as safe
    assert conf.alpha == 1.5
    assert conf.beta == 1.5


def test_confidence_mean():
    conf = BetaConfidence(alpha=3.0, beta=1.0)
    assert conf.mean() == pytest.approx(0.75)


def test_set_threshold():
    conf = BetaConfidence()
    conf.set_threshold(0.8)
    assert conf.get_threshold() == 0.8
