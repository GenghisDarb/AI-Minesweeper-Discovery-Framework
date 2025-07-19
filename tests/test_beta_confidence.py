import pytest
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_update():
    conf = BetaConfidence()
    conf.update(0.5, True)  # Predicted 50% mine, revealed as mine
    # after update(predicted_prob=0.5, actual_mine=True)
    assert conf.alpha > conf.beta  # confidence up

    conf.update(0.5, False)  # Predicted 50% mine, revealed as safe
    # after update(predicted_prob=0.5, actual_mine=False)
    assert conf.alpha <= conf.beta  # confidence down or unchanged

    conf.update(1.0, True)  # Full confidence mine, revealed as mine
    assert conf.alpha > conf.beta  # confidence up


def test_confidence_mean():
    conf = BetaConfidence(alpha=3.0, beta=1.0)
    assert conf.mean() == pytest.approx(0.75)


def test_set_threshold():
    conf = BetaConfidence()
    conf.set_threshold(0.8)
    assert conf.get_threshold() == 0.8
