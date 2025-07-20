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

    conf.update(success=True)
    assert conf.alpha > conf.beta

    conf.update(success=False)
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

    conf.update(success=True)
    assert conf.mean() > 0.5

    conf.update(success=False)
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
