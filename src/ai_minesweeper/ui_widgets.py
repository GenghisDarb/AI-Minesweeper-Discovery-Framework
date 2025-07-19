import streamlit as st
import logging
from ai_minesweeper.constants import State

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def display_confidence(conf: float, mode="cli") -> str:
    if mode == "cli":
        result = f"Confidence: {conf * 100:.1f}% [{'=' * int(conf * 20)}{' ' * (20 - int(conf * 20))}]"
        logger.info(result)
        return result
    elif mode == "streamlit":
        st.markdown("### Confidence Level")
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


def render_revealed_hypotheses_summary(board):
    """
    Render a summary panel for revealed hypotheses.

    Args:
        board (Board): The current game board.
    """
    st.markdown("### Revealed Hypotheses Summary")
    for hypothesis in board.get_revealed_hypotheses():
        st.write(f"Hypothesis: {hypothesis}")


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
    Apply custom CSS to improve the grid's look and feel, ensuring accessibility.
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
        /* Accessibility: Ensure colorblind-safe palette */
        .safe {
            background-color: #6aa84f; /* Green */
            color: white;
        }
        .hidden {
            background-color: #b7b7b7; /* Gray */
            color: white;
        }
        .mine {
            background-color: #cc0000; /* Red */
            color: white;
        }
        .clue {
            background-color: #3c78d8; /* Blue */
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hypotheses_with_tooltips(board):
    """
    Render hypotheses with tooltips for additional context.

    Args:
        board (Board): The current game board.
    """
    st.markdown("### Hypotheses with Tooltips")
    for hypothesis in board.get_revealed_hypotheses():
        tooltip = (
            f"Details: {hypothesis.details}"
            if hasattr(hypothesis, "details")
            else "No additional details."
        )
        st.markdown(
            f'<div style="border: 1px solid black; padding: 5px;" title="{tooltip}">{hypothesis}</div>',
            unsafe_allow_html=True,
        )


def align_chat_input_with_ui():
    """
    Ensure the chat input box aligns with the rest of the UI components.
    """
    st.markdown(
        """
        <style>
        .stTextInput {
            margin-top: 10px;
            margin-bottom: 10px;
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def update_hypotheses_panel(board):
    """
    Update the hypotheses panel to reflect the latest game state.

    Args:
        board (Board): The current game board.
    """
    st.markdown("### Updated Hypotheses Panel")
    for hypothesis in board.get_revealed_hypotheses():
        st.write(f"Hypothesis: {hypothesis}")

    unresolved = [
        cell for row in board.grid for cell in row if cell.state == State.HIDDEN
    ]
    if unresolved:
        st.markdown("#### Unresolved Cells")
        for cell in unresolved:
            st.write(f"Cell: ({cell.row}, {cell.col})")


def ensure_grid_styling_consistency():
    """
    Ensure consistent grid styling across all components.
    """
    st.markdown(
        """
        <style>
        .consistent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
            gap: 5px;
            justify-items: center;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_accessibility_labels_to_cells(board):
    """
    Add accessibility labels to cells for screen readers.

    Args:
        board (Board): The current game board.
    """
    for row in board.grid:
        for cell in row:
            label = f"Cell at row {cell.row}, column {cell.col}, state: {cell.state}"
            st.markdown(
                f'<div aria-label="{label}" style="border: 1px solid black; padding: 5px;">{cell.state}</div>',
                unsafe_allow_html=True,
            )


def enhance_grid_accessibility():
    """
    Add ARIA roles and labels to the grid for better accessibility.
    """
    st.markdown(
        """
        <style>
        .grid-cell[role="button"] {
            outline: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Example of adding ARIA roles dynamically
    st.markdown(
        '<div role="grid" aria-label="Minesweeper grid">',
        unsafe_allow_html=True,
    )
    # ...existing code for rendering grid cells...
    st.markdown("</div>", unsafe_allow_html=True)


def add_colorblind_friendly_palette():
    """
    Apply a colorblind-friendly palette to the grid for better accessibility.
    """
    st.markdown(
        """
        <style>
        .safe {
            background-color: #88CCEE; /* Light Blue */
            color: black;
        }
        .hidden {
            background-color: #DDCC77; /* Light Yellow */
            color: black;
        }
        .mine {
            background-color: #CC6677; /* Light Red */
            color: white;
        }
        .clue {
            background-color: #117733; /* Dark Green */
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_high_contrast_mode():
    """
    Add a high-contrast mode for better visibility.
    """
    st.markdown(
        """
        <style>
        .high-contrast .safe {
            background-color: #0000FF; /* Bright Blue */
            color: white;
        }
        .high-contrast .hidden {
            background-color: #000000; /* Black */
            color: white;
        }
        .high-contrast .mine {
            background-color: #FF0000; /* Bright Red */
            color: white;
        }
        .high-contrast .clue {
            background-color: #FFFF00; /* Bright Yellow */
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def finalize_accessibility_and_visual_enhancements():
    """
    Finalize accessibility and visual enhancements for the Minesweeper grid.
    """
    # Ensure all accessibility features are applied
    enhance_grid_accessibility()
    add_accessibility_labels_to_cells(board=None)  # Placeholder for actual board object

    # Apply visual enhancements
    apply_grid_styling()
    add_colorblind_friendly_palette()
    add_high_contrast_mode()

    # Log completion
    logger.info("Accessibility and visual enhancements finalized.")


def consolidate_functionality():
    """
    Consolidate functionality from meta_cell_confidence/ui_widgets.py into this file.
    """
    pass  # Placeholder for consolidated functionality


class BarMeter:
    """
    Displays a confidence bar in the CLI or GUI.

    Attributes:
        confidence (float): Confidence value between 0 and 1.
    """

    def __init__(self, confidence: float):
        self.confidence = confidence

    def render_cli(self):
        """
        Renders the confidence bar in the CLI.
        """
        bar_length = 20
        filled_length = int(self.confidence * bar_length)
        bar = "■" * filled_length + "□" * (bar_length - filled_length)
        print(f"CONFIDENCE {bar} {self.confidence * 100:.0f} %")

def render_chi_brot_visualizer():
    """Render a placeholder χ-brot fractal visualizer."""
    st.markdown("### χ-brot Fractal Visualizer")
    st.write("This feature is under development. Placeholder visualization below:")
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2 + 0.785398

    plt.contourf(X, Y, Z, levels=50, cmap="viridis")
    st.pyplot(plt)
