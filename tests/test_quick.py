import pytest
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.cell import State
from ai_minesweeper.config import DEBUG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to your periodic table hypothesis grid
CSV_PATH = "examples/periodic_table/elements.csv"

# Debugging check for config import
logger.info(f"[TEST CHECK] DEBUG variable in test_quick.py: {DEBUG}")

def test_risk_assessor_estimate_structure():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    prob_map = assessor.estimate(board)

    assert isinstance(prob_map, dict)
    assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in prob_map), "Keys in prob_map should be coordinate tuples"
    assert all(isinstance(p, float) for p in prob_map.values()), "Values in prob_map should be floats"

def test_risk_assessor_estimate_behavior():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    prob_map = assessor.estimate(board)

    logger.info(f"[TEST SETUP] Passing board object: {board} class={board.__class__}")
    logger.info(f"[TEST SETUP] Sample cell (0,0): {board.grid[0][0]} state={board.grid[0][0].state}")

    hidden_cells = [(r, c) for (r, c) in prob_map.keys() if board.grid[r][c].is_hidden()]
    logger.info(f"[CALLER] Got {len(hidden_cells)} hidden cells: {[ (r, c) for r, c in hidden_cells ]}")
    assert len(hidden_cells) > 0, "Expected some hidden cells in the estimate result"

def test_risk_assessor_choose_move_returns_hidden():
    board = BoardBuilder.from_csv(CSV_PATH)
    assessor = RiskAssessor()
    move = assessor.choose_move(board)

    assert move is not None, "Expected a move to be returned"
    r, c = move
    assert board.grid[r][c].is_hidden(), f"Cell {r,c} was not hidden when selected"

def test_render_cell_with_tooltip():
    from src.ai_minesweeper.ui_widgets import render_cell_with_tooltip
    html = render_cell_with_tooltip("safe", "This cell is safe.")
    assert "background-color: green" in html
    assert "This cell is safe." in html

logger.debug(f"[DEBUG] State.HIDDEN id = {id(State.HIDDEN)} in test_quick")
