from ai_minesweeper.ui_widgets import rank_hypotheses_core

def test_rank_hypotheses_core_deterministic():
    inp = [
        "mine at (3,4)",
        "safe (0,0)",
        "flag corner",
        "reveal center",
    ]
    out1 = rank_hypotheses_core(inp)
    out2 = rank_hypotheses_core(inp)
    assert out1 == out2
    assert set(out1) == set(inp)
