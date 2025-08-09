from ai_minesweeper.ui_widgets import rank_hypotheses_core


def test_rank_hypotheses_core_deterministic_and_permutation():
    hyps = ["H2", "A", "H10", "B", "A1", "A10", "A2"]
    out1 = rank_hypotheses_core(hyps)
    out2 = rank_hypotheses_core(list(reversed(hyps)))
    # Deterministic and order independent with the same key
    assert out1 == out2
    # Same multiset
    assert sorted(out1) == sorted(hyps)
