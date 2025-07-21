import pytest

from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence


def test_confidence_update():
    conf = BetaConfidence()

    # Valid updates
    conf.update(0.5, True)  # Predicted 50% mine, revealed as mine
    assert conf.alpha > conf.beta  # confidence up

    conf.update(0.5, False)  # Predicted 50% mine, revealed as safe
    assert conf.alpha <= conf.beta  # confidence down or unchanged

    conf.update(1.0, True)  # Full confidence mine, revealed as mine
    assert conf.alpha > conf.beta  # confidence up

    conf.update(prob_pred=0.9, revealed_is_mine=True)
    assert conf.alpha > conf.beta

    # Invalid updates
    with pytest.raises(ValueError):
        conf.update(-0.1, True)  # Invalid probability

    with pytest.raises(ValueError):
        conf.update(1.1, False)  # Invalid probability

    with pytest.raises(ValueError):
        conf.update()  # Missing parameters


def test_confidence_mean():
    conf = BetaConfidence()
    assert conf.mean() == pytest.approx(0.5)

    conf.update(0.5, True)  # Correct usage of update method
    assert conf.mean() > 0.5

    conf.update(0.5, False)  # Correct usage of update method
    assert conf.mean() < 0.5


def test_set_and_get_threshold():
    conf = BetaConfidence()

    # Valid threshold
    conf.set_threshold(0.8)
    assert conf.get_threshold() == 0.8

    # Invalid threshold
    with pytest.raises(ValueError):
        conf.set_threshold(-0.1)

    with pytest.raises(ValueError):
        conf.set_threshold(1.1)

    # Threshold not set
    conf = BetaConfidence()
    assert conf.get_threshold() is None


def test_beta_confidence():
    conf = BetaConfidence()
    assert conf.mean() == 0.5

    # Simulate successful prediction
    conf.update(0.9, True)  # Correct usage of update method
    assert conf.alpha == 2.0
    assert conf.beta == 1.0

    # Simulate failed prediction
    conf.update(0.1, False)  # Correct usage of update method
    assert conf.alpha == 2.0
    assert conf.beta == 2.0


def test_beta_confidence_threshold():
    conf = BetaConfidence()
    conf.set_threshold(0.7)
    assert conf.get_threshold() == 0.7

    with pytest.raises(ValueError):
        conf.set_threshold(1.5)
