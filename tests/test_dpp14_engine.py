from ai_minesweeper.torus_recursion.dpp14_recursion_engine import DPP14RecursionEngine
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import RiskAssessor
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "examples" / "boards"


def test_dpp14_engine_phase_locked():
    """Test the 14-lane engine on a simple board where all lanes should converge."""
    board = BoardBuilder.from_csv(FIXTURE_DIR / "simple.csv")
    engine = DPP14RecursionEngine(board, RiskAssessor)
    results = engine.run()

    assert results["final_chi14"] is not None
    assert len(results["collapsed_lanes"]) == 0  # No lanes should collapse
    assert all(isinstance(lane, int) for lane in results["collapsed_lanes"])


def test_dpp14_engine_divergence():
    """Test the 14-lane engine on a board that forces divergence."""
    board = BoardBuilder.from_csv(FIXTURE_DIR / "divergent.csv")
    engine = DPP14RecursionEngine(board, RiskAssessor)
    results = engine.run()

    assert len(results["collapsed_lanes"]) > 0  # Some lanes should collapse
    assert results["final_chi14"] is not None
