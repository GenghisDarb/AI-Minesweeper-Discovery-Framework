import pytest
from ai_minesweeper.torus_recursion.dpp14_recursion_engine import DPP14RecursionEngine
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import RiskAssessor

def test_dpp14_engine_phase_locked():
    """Test the 14-lane engine on a simple board where all lanes should converge."""
    board = BoardBuilder.from_csv("examples/boards/simple.csv")
    engine = DPP14RecursionEngine(board, RiskAssessor)
    results = engine.run()

    assert results["final_chi14"] is not None
    assert len(results["collapsed_lanes"]) == 0  # No lanes should collapse

def test_dpp14_engine_divergence():
    """Test the 14-lane engine on a board that forces divergence."""
    board = BoardBuilder.from_csv("examples/boards/divergent.csv")
    engine = DPP14RecursionEngine(board, RiskAssessor)
    results = engine.run()

    assert len(results["collapsed_lanes"]) > 0  # Some lanes should collapse
    assert results["final_chi14"] is not None
