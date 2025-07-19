import pytest
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_update():
    conf = BetaConfidence()
    conf.update(0.5, True)  # Predicted 50% mine, revealed as mine
    assert abs(conf.alpha - 1.5) < 0.1
    assert abs(conf.beta - 1.5) < 0.1  # Both alpha and beta increase by 0.5

    conf.update(0.5, False)  # Predicted 50% mine, revealed as safe
    assert abs(conf.alpha - 2.0) < 0.1  # alpha += (1 - 0.5) = 0.5
    assert abs(conf.beta - 2.0) < 0.1   # beta += 0.5

    conf.update(1.0, True)  # Full confidence mine, revealed as mine
    assert abs(conf.alpha - 3.0) < 0.1  # alpha += 1.0
    assert abs(conf.beta - 2.0) < 0.1   # beta += (1 - 1.0) = 0


def test_confidence_mean():
    conf = BetaConfidence(alpha=3.0, beta=1.0)
    assert conf.mean() == pytest.approx(0.75)


def test_set_threshold():
    conf = BetaConfidence()
    conf.set_threshold(0.8)
    assert conf.get_threshold() == 0.8
