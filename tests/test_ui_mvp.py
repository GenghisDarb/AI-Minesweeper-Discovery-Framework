import os

from ai_minesweeper.ui_widgets import chi_brot_visualization


def test_chi_brot_visualization_writes_png(tmp_path, monkeypatch):
    # Ensure working dir is temporary to avoid polluting repo
    monkeypatch.chdir(tmp_path)
    # Pass None to use default chi=0 path deterministically
    out = chi_brot_visualization(None)  # type: ignore[arg-type]
    assert out.endswith("chi_brot.png")
    assert os.path.exists(out)
    # File should be non-empty
    assert os.path.getsize(out) > 100
