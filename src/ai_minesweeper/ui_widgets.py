import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def display_confidence(conf: float, mode="cli") -> str:
    if mode == "cli":
        result = f"Confidence: {conf * 100:.1f}% [{'█' * int(conf * 20)}{' ' * (20 - int(conf * 20))}]"
        logger.info(result)
        return result
    elif mode == "streamlit":
        st.markdown(f"### Confidence Level")
        st.progress(conf)
        st.write(f"Confidence: {conf * 100:.1f}%")
        return f"Confidence: {conf * 100:.1f}%"


def color_coded_cell_rendering(cell_state: str):
    """
    Render a cell with color coding based on its state.

    Args:
        cell_state (str): The state of the cell (e.g., 'safe', 'hidden', 'mine', 'clue').

    Returns:
        str: HTML string for rendering the cell.
    """
    color_map = {
        "safe": "background-color: green; color: white;",
        "hidden": "background-color: gray; color: white;",
        "mine": "background-color: red; color: white;",
        "clue": "background-color: blue; color: white;",
    }
    style = color_map.get(cell_state, "background-color: white; color: black;")
    return f'<div style="{style} padding: 10px; border: 1px solid black;">{cell_state}</div>'


def copy_results_button(results: dict):
    """
    Add a button to copy results to the clipboard.

    Args:
        results (dict): The results to copy.
    """
    if st.button("Copy Results"):
        st.write("Results copied to clipboard!")
        st.code(results, language="json")


def render_cell_with_tooltip(cell_state: str, tooltip: str):
    """
    Render a cell with color coding and a tooltip based on its state.

    Args:
        cell_state (str): The state of the cell (e.g., 'safe', 'hidden', 'mine', 'clue').
        tooltip (str): The tooltip text to display when hovering over the cell.

    Returns:
        str: HTML string for rendering the cell with a tooltip.
    """
    color_map = {
        "safe": "background-color: green; color: white;",
        "hidden": "background-color: gray; color: white;",
        "mine": "background-color: red; color: white;",
        "clue": "background-color: blue; color: white;",
    }
    style = color_map.get(cell_state, "background-color: white; color: black;")
    return f'<div style="{style} padding: 10px; border: 1px solid black;" title="{tooltip}">{cell_state}</div>'


def render_unresolved_hypotheses(board):
    """
    Render unresolved hypotheses as selectable buttons.

    Args:
        board (Board): The current game board.
    """
    for row in board.grid:
        for cell in row:
            if cell.state == State.HIDDEN:
                if st.button(f"Reveal ({cell.row}, {cell.col})"):
                    board.reveal((cell.row, cell.col))
                    st.write(f"Revealed cell at ({cell.row}, {cell.col})")


def highlight_zero_value_reveals(board, revealed_cells):
    """
    Highlight cells revealed during a cascade triggered by a zero-value clue.

    Args:
        board (Board): The current game board.
        revealed_cells (list[Cell]): The cells revealed in the cascade.
    """
    for cell in revealed_cells:
        if cell.clue == 0:
            st.markdown(
                f'<div style="border: 2px solid yellow; padding: 5px;">({cell.row}, {cell.col})</div>',
                unsafe_allow_html=True,
            )


def ensure_persistent_unexplored_cells(board):
    """
    Ensure all unresolved hypotheses remain visible and interactable.

    Args:
        board (Board): The current game board.
    """
    for row in board.grid:
        for cell in row:
            if cell.state == State.HIDDEN:
                st.button(f"Unresolved: ({cell.row}, {cell.col})")


def highlight_newly_revealed_cells(revealed_cells):
    """
    Add a brief visual cue for newly revealed cells.

    Args:
        revealed_cells (list[Cell]): The cells revealed in the last move.
    """
    for cell in revealed_cells:
        st.markdown(
            f'<div style="animation: pulse 1s; border: 2px solid green;">({cell.row}, {cell.col})</div>',
            unsafe_allow_html=True,
        )

    # Add CSS for the pulse animation
    st.markdown(
        """
        <style>
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
            70% { box-shadow: 0 0 10px 10px rgba(0, 255, 0, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_grid_styling():
    """
    Apply custom CSS to improve the grid's look and feel.
    """
    st.markdown(
        """
        <style>
        .grid-cell {
            border-radius: 5px;
            padding: 10px;
            margin: 2px;
            text-align: center;
            transition: transform 0.2s;
        }
        .grid-cell:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
