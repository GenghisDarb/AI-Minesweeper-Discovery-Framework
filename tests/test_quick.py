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

def test_add_accessibility_labels_to_cells():
    from src.ai_minesweeper.ui_widgets import add_accessibility_labels_to_cells
    from ai_minesweeper.board_builder import BoardBuilder

    board = BoardBuilder.from_csv(CSV_PATH)
    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        add_accessibility_labels_to_cells(board)
    except Exception as e:
        pytest.fail(f"add_accessibility_labels_to_cells raised an exception: {e}")

def test_update_hypotheses_panel():
    from src.ai_minesweeper.ui_widgets import update_hypotheses_panel
    from ai_minesweeper.board_builder import BoardBuilder

    board = BoardBuilder.from_csv(CSV_PATH)
    # Mock Streamlit's markdown and write functions
    st.markdown = lambda x: None
    st.write = lambda x: None

    try:
        update_hypotheses_panel(board)
    except Exception as e:
        pytest.fail(f"update_hypotheses_panel raised an exception: {e}")

def test_ensure_grid_styling_consistency():
    from src.ai_minesweeper.ui_widgets import ensure_grid_styling_consistency

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        ensure_grid_styling_consistency()
    except Exception as e:
        pytest.fail(f"ensure_grid_styling_consistency raised an exception: {e}")

def test_align_chat_input_with_ui():
    from src.ai_minesweeper.ui_widgets import align_chat_input_with_ui

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        align_chat_input_with_ui()
    except Exception as e:
        pytest.fail(f"align_chat_input_with_ui raised an exception: {e}")

def test_render_hypotheses_with_tooltips():
    from src.ai_minesweeper.ui_widgets import render_hypotheses_with_tooltips
    from ai_minesweeper.board_builder import BoardBuilder

    board = BoardBuilder.from_csv(CSV_PATH)
    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        render_hypotheses_with_tooltips(board)
    except Exception as e:
        pytest.fail(f"render_hypotheses_with_tooltips raised an exception: {e}")

def test_highlight_zero_value_reveals():
    from src.ai_minesweeper.ui_widgets import highlight_zero_value_reveals
    from ai_minesweeper.board_builder import BoardBuilder
    from ai_minesweeper.cell import Cell

    board = BoardBuilder.from_csv(CSV_PATH)
    revealed_cells = [Cell(row=0, col=0, clue=0), Cell(row=1, col=1, clue=0)]

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        highlight_zero_value_reveals(board, revealed_cells)
    except Exception as e:
        pytest.fail(f"highlight_zero_value_reveals raised an exception: {e}")

def test_ensure_persistent_unexplored_cells():
    from src.ai_minesweeper.ui_widgets import ensure_persistent_unexplored_cells
    from ai_minesweeper.board_builder import BoardBuilder

    board = BoardBuilder.from_csv(CSV_PATH)

    # Mock Streamlit's button function
    st.button = lambda x: None

    try:
        ensure_persistent_unexplored_cells(board)
    except Exception as e:
        pytest.fail(f"ensure_persistent_unexplored_cells raised an exception: {e}")

def test_highlight_newly_revealed_cells():
    from src.ai_minesweeper.ui_widgets import highlight_newly_revealed_cells
    from ai_minesweeper.cell import Cell

    revealed_cells = [Cell(row=0, col=0), Cell(row=1, col=1)]

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        highlight_newly_revealed_cells(revealed_cells)
    except Exception as e:
        pytest.fail(f"highlight_newly_revealed_cells raised an exception: {e}")

def test_apply_grid_styling():
    from src.ai_minesweeper.ui_widgets import apply_grid_styling

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        apply_grid_styling()
    except Exception as e:
        pytest.fail(f"apply_grid_styling raised an exception: {e}")

def test_add_high_contrast_mode():
    from src.ai_minesweeper.ui_widgets import add_high_contrast_mode

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        add_high_contrast_mode()
    except Exception as e:
        pytest.fail(f"add_high_contrast_mode raised an exception: {e}")

def test_add_colorblind_friendly_palette():
    from src.ai_minesweeper.ui_widgets import add_colorblind_friendly_palette

    # Mock Streamlit's markdown function
    st.markdown = lambda x, unsafe_allow_html: None

    try:
        add_colorblind_friendly_palette()
    except Exception as e:
        pytest.fail(f"add_colorblind_friendly_palette raised an exception: {e}")

logger.debug(f"[DEBUG] State.HIDDEN id = {id(State.HIDDEN)} in test_quick")
