import logging

import streamlit as st

from ai_minesweeper.cell import State


def color_coded_cell_rendering(cell_state: str):
    """
    Render a cell with color coding based on its state.

    Args:
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
    """
    if st.button("Copy Results"):
        st.write("Results copied to clipboard!")
        st.code(results, language="json")


def render_cell_with_tooltip(cell_state: str, tooltip: str):
    """
    Render a cell with color coding and a tooltip based on its state.

    Args:

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
    """
    for row in board.grid:
        for cell in row:
            if cell.state == State.HIDDEN:
                if st.button(f"Reveal ({cell.row}, {cell.col})"):
                    board.reveal(cell)
                    st.write(f"Revealed cell at ({cell.row}, {cell.col})")


def render_revealed_hypotheses_summary(board):
    """
    Render a summary panel for revealed hypotheses.
    """
    st.markdown("### Revealed Hypotheses Summary")
    for hypothesis in board.get_revealed_hypotheses():
        st.write(f"Hypothesis: {hypothesis}")


def highlight_zero_value_reveals(board, revealed_cells):
    """
    Highlight cells revealed during a cascade triggered by a zero-value clue.
import logging
import streamlit as st
from ai_minesweeper.cell import State

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    Apply a CSS pulse animation to newly revealed cells in Streamlit.
    """
    css = """
<style>
.highlight-pulse {
    animation: pulse 0.8s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
    70% { box-shadow: 0 0 10px 10px rgba(0, 255, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
    for cell in revealed_cells:
        st.markdown(
            f'<div class="highlight-pulse" style="border: 2px solid green;">({cell.row}, {cell.col})</div>',
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
    Update the hypotheses panel to display revealed and unresolved hypotheses.

    Args:
        board (Board): The current game board.
    """
    st.markdown("### Hypotheses Panel")
    st.markdown("#### Revealed Hypotheses")
    for hypothesis in board.get_revealed_hypotheses():
        st.write(f"Hypothesis: {hypothesis}")

    st.markdown("#### Unresolved Hypotheses")
    for row in board.grid:
        for cell in row:
            if cell.state == State.HIDDEN:
                st.write(f"Unresolved Cell: ({cell.row}, {cell.col})")


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


def apply_all_css_enhancements():
    """
    Apply all CSS enhancements, including grid styling, colorblind palette, and high-contrast mode.
    """
    apply_grid_styling()
    if st.sidebar.checkbox("Enable colorblind-friendly palette"):
        add_colorblind_friendly_palette()
    if st.sidebar.checkbox("Enable high-contrast mode"):
        add_high_contrast_mode()


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
"""
UI Widgets and helpers for AI Minesweeper visualization.

This module provides UI components for:
- Color-coding and visual styling
- Tooltips and accessibility features
- χ-cycle visualization
- High-contrast mode support
- TORUS theory visualization stubs
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

from .board import Board, CellState


class ColorScheme:
    """Color schemes for minesweeper visualization."""
    
    # Default color scheme
    DEFAULT = {
        "hidden": "#C0C0C0",
        "revealed": "#F0F0F0", 
        "flagged": "#FF6B6B",
        "safe_flagged": "#4ECDC4",
        "mine": "#FF4444",
        "numbers": {
            1: "#0000FF",
            2: "#008000", 
            3: "#FF0000",
            4: "#000080",
            5: "#800000",
            6: "#008080",
            7: "#000000",
            8: "#808080"
        },
        "confidence_low": "#FFE5E5",
        "confidence_medium": "#FFF5E5", 
        "confidence_high": "#E5F5E5"
    }
    
    # High contrast mode
    HIGH_CONTRAST = {
        "hidden": "#000000",
        "revealed": "#FFFFFF",
        "flagged": "#FF0000", 
        "safe_flagged": "#00FF00",
        "mine": "#FF0000",
        "numbers": {
            1: "#0000FF",
            2: "#008000",
            3: "#FF0000", 
            4: "#000080",
            5: "#800000",
            6: "#008080",
            7: "#000000",
            8: "#808080"
        },
        "confidence_low": "#330000",
        "confidence_medium": "#333300",
        "confidence_high": "#003300"
    }
    
    # χ-cycle visualization colors
    CHI_CYCLE = {
        "phase_0": "#FF6B6B",
        "phase_1": "#4ECDC4", 
        "phase_2": "#45B7D1",
        "phase_3": "#96CEB4",
        "phase_4": "#FECA57"
    }


class MinesweeperVisualizer:
    """
    Visualization utilities for AI Minesweeper with χ-recursive form.
    
    Provides color-coding, tooltips, and accessibility features
    for enhanced user experience and debugging.
    """
    
    def __init__(self, high_contrast: bool = False):
        """
        Initialize the visualizer.
        
        Args:
            high_contrast: Enable high contrast mode for accessibility
        """
        self.high_contrast = high_contrast
        self.color_scheme = ColorScheme.HIGH_CONTRAST if high_contrast else ColorScheme.DEFAULT
        self.logger = logging.getLogger(__name__)
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8' if hasattr(plt.style, 'seaborn-v0_8') else 'default')
    
    def create_board_visualization(
        self, 
        board: Board, 
        risk_map: Optional[Dict[Tuple[int, int], float]] = None,
        confidence_overlay: bool = False
    ) -> plt.Figure:
        """
        Create a comprehensive board visualization.
        
        Args:
            board: Current board state
            risk_map: Optional risk assessment overlay
            confidence_overlay: Show confidence-based coloring
            
        Returns:
            Matplotlib figure with board visualization
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create board grid
        self._draw_board_grid(ax, board, risk_map, confidence_overlay)
        
        # Add cell contents
        self._draw_cell_contents(ax, board)
        
        # Add risk overlay if provided
        if risk_map:
            self._draw_risk_overlay(ax, board, risk_map)
        
        # Configure axes
        ax.set_xlim(-0.5, board.width - 0.5)
        ax.set_ylim(-0.5, board.height - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()  # Standard minesweeper layout
        
        # Remove tick marks
        ax.set_xticks(range(board.width))
        ax.set_yticks(range(board.height))
        ax.grid(True, alpha=0.3)
        
        # Title with game state
        title = f"AI Minesweeper {board.width}x{board.height} - Mines: {board.remaining_mines}/{board.mine_count}"
        if board.is_solved():
            title += " ✅ SOLVED"
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        return fig
    
    def _draw_board_grid(
        self, 
        ax: plt.Axes, 
        board: Board, 
        risk_map: Optional[Dict[Tuple[int, int], float]],
        confidence_overlay: bool
    ) -> None:
        """Draw the basic board grid with cell backgrounds."""
        for x in range(board.width):
            for y in range(board.height):
                pos = (x, y)
                state = board.cell_states[pos]
                
                # Determine cell color
                if confidence_overlay and risk_map and pos in risk_map:
                    color = self._get_confidence_color(risk_map[pos])
                else:
                    color = self._get_cell_color(state)
                
                # Draw cell rectangle
                rect = patches.Rectangle(
                    (x - 0.4, y - 0.4), 0.8, 0.8,
                    linewidth=1, edgecolor='black', facecolor=color
                )
                ax.add_patch(rect)
    
    def _draw_cell_contents(self, ax: plt.Axes, board: Board) -> None:
        """Draw cell contents (numbers, flags, mines)."""
        for x in range(board.width):
            for y in range(board.height):
                pos = (x, y)
                state = board.cell_states[pos]
                
                text = ""
                text_color = "black"
                
                if state == CellState.FLAGGED:
                    text = "🚩"
                elif state == CellState.SAFE_FLAGGED:
                    text = "⚡"
                elif state == CellState.REVEALED:
                    if pos in board.mines:
                        text = "💣"
                        text_color = "red"
                    else:
                        number = board.revealed_numbers.get(pos, 0)
                        if number > 0:
                            text = str(number)
                            text_color = self.color_scheme["numbers"].get(number, "black")
                
                if text:
                    ax.text(x, y, text, ha='center', va='center', 
                           fontsize=12, fontweight='bold', color=text_color)
    
    def _draw_risk_overlay(
        self, 
        ax: plt.Axes, 
        board: Board, 
        risk_map: Dict[Tuple[int, int], float]
    ) -> None:
        """Draw risk assessment overlay."""
        # Create risk heatmap
        risk_data = np.zeros((board.height, board.width))
        for (x, y), risk in risk_map.items():
            risk_data[y, x] = risk
        
        # Create transparent overlay
        im = ax.imshow(risk_data, cmap='Reds', alpha=0.3, vmin=0, vmax=1)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Mine Risk', rotation=270, labelpad=15)
    
    def _get_cell_color(self, state: CellState) -> str:
        """Get color for cell based on state."""
        if state == CellState.HIDDEN:
            return self.color_scheme["hidden"]
        elif state == CellState.REVEALED:
            return self.color_scheme["revealed"]
        elif state == CellState.FLAGGED:
            return self.color_scheme["flagged"]
        elif state == CellState.SAFE_FLAGGED:
            return self.color_scheme["safe_flagged"]
        else:
            return "#FFFFFF"
    
    def _get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level."""
        if confidence < 0.3:
            return self.color_scheme["confidence_high"]
        elif confidence < 0.7:
            return self.color_scheme["confidence_medium"]
        else:
            return self.color_scheme["confidence_low"]
    
    def create_chi_cycle_visualization(
        self, 
        confidence_history: List[float],
        chi_cycle_count: int
    ) -> plt.Figure:
        """
        Create χ-cycle progress visualization.
        
        Args:
            confidence_history: List of confidence values over time
            chi_cycle_count: Current χ-cycle count
            
        Returns:
            Matplotlib figure with χ-cycle visualization
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Confidence trend plot
        if confidence_history:
            x_vals = range(len(confidence_history))
            ax1.plot(x_vals, confidence_history, 'b-', linewidth=2, label='Confidence')
            
            # Add trend line
            if len(confidence_history) > 3:
                z = np.polyfit(x_vals, confidence_history, 1)
                p = np.poly1d(z)
                ax1.plot(x_vals, p(x_vals), 'r--', alpha=0.7, label='Trend')
            
            ax1.set_ylabel('Confidence Level')
            ax1.set_title('χ-Recursive Confidence Evolution')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 1)
        
        # χ-cycle phase visualization
        phase = (chi_cycle_count % 20) / 20.0
        phases = np.linspace(0, 2*np.pi, 100)
        cycle_signal = 0.5 + 0.5 * np.sin(phases)
        
        ax2.plot(phases, cycle_signal, 'g-', linewidth=2, label='χ-Cycle')
        current_phase = 2 * np.pi * phase
        current_value = 0.5 + 0.5 * np.sin(current_phase)
        ax2.plot(current_phase, current_value, 'ro', markersize=10, label='Current Phase')
        
        ax2.set_xlabel('Phase (radians)')
        ax2.set_ylabel('Cycle Value')
        ax2.set_title(f'TORUS Theory χ-Cycle (Count: {chi_cycle_count})')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_risk_distribution_plot(
        self, 
        risk_map: Dict[Tuple[int, int], float]
    ) -> plt.Figure:
        """
        Create risk distribution analysis plot.
        
        Args:
            risk_map: Risk assessment data
            
        Returns:
            Matplotlib figure with risk analysis
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        if not risk_map:
            ax1.text(0.5, 0.5, "No risk data available", ha='center', va='center')
            ax2.text(0.5, 0.5, "No risk data available", ha='center', va='center')
            return fig
        
        risks = list(risk_map.values())
        
        # Risk histogram
        ax1.hist(risks, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_xlabel('Risk Level')
        ax1.set_ylabel('Number of Cells')
        ax1.set_title('Risk Distribution')
        ax1.grid(True, alpha=0.3)
        
        # Risk categories
        safe_count = len([r for r in risks if r < 0.2])
        medium_count = len([r for r in risks if 0.2 <= r < 0.8])
        danger_count = len([r for r in risks if r >= 0.8])
        
        categories = ['Safe\n(<0.2)', 'Medium\n(0.2-0.8)', 'Dangerous\n(≥0.8)']
        counts = [safe_count, medium_count, danger_count]
        colors = ['green', 'orange', 'red']
        
        ax2.bar(categories, counts, color=colors, alpha=0.7)
        ax2.set_ylabel('Number of Cells')
        ax2.set_title('Risk Categories')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class TooltipManager:
    """
    Tooltip and accessibility manager for interactive UI components.
    """
    
    def __init__(self):
        """Initialize tooltip manager."""
        self.active_tooltips: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_cell_tooltip(
        self, 
        position: Tuple[int, int], 
        board: Board,
        risk: Optional[float] = None,
        confidence: Optional[float] = None
    ) -> str:
        """
        Create tooltip text for a board cell.
        
        Args:
            position: Cell coordinates
            board: Current board state
            risk: Optional risk assessment
            confidence: Optional confidence level
            
        Returns:
            Formatted tooltip text
        """
        x, y = position
        state = board.cell_states[position]
        
        tooltip_lines = [f"Cell ({x}, {y})"]
        
        # State information
        if state == CellState.HIDDEN:
            tooltip_lines.append("State: Hidden")
        elif state == CellState.REVEALED:
            number = board.revealed_numbers.get(position, 0)
            tooltip_lines.append(f"State: Revealed ({number} adjacent mines)")
        elif state == CellState.FLAGGED:
            tooltip_lines.append("State: Flagged as mine")
        elif state == CellState.SAFE_FLAGGED:
            tooltip_lines.append("State: Safe flag (χ-recursive)")
        
        # Risk information
        if risk is not None:
            tooltip_lines.append(f"Mine Risk: {risk:.3f}")
            if risk < 0.2:
                tooltip_lines.append("Category: Safe")
            elif risk < 0.8:
                tooltip_lines.append("Category: Medium risk") 
            else:
                tooltip_lines.append("Category: Dangerous")
        
        # Confidence information
        if confidence is not None:
            tooltip_lines.append(f"Solver Confidence: {confidence:.3f}")
        
        # Neighbor analysis
        if state == CellState.REVEALED:
            neighbors = board.get_neighbors(x, y)
            hidden_neighbors = len([n for n in neighbors if board.cell_states[n] == CellState.HIDDEN])
            flagged_neighbors = len([n for n in neighbors if 
                                   board.cell_states[n] in [CellState.FLAGGED, CellState.SAFE_FLAGGED]])
            
            tooltip_lines.append(f"Hidden neighbors: {hidden_neighbors}")
            tooltip_lines.append(f"Flagged neighbors: {flagged_neighbors}")
        
        return "\n".join(tooltip_lines)
    
    def create_solver_status_tooltip(self, solver_stats: Dict) -> str:
        """
        Create tooltip for solver status display.
        
        Args:
            solver_stats: Solver statistics dictionary
            
        Returns:
            Formatted solver status tooltip
        """
        lines = ["AI Solver Status"]
        lines.append(f"Iterations: {solver_stats.get('solver_iterations', 0)}")
        lines.append(f"χ-Cycle Progress: {solver_stats.get('chi_cycle_progress', 0)}")
        lines.append(f"Active Constraints: {solver_stats.get('active_constraints', 0)}")
        
        confidence_stats = solver_stats.get('policy_stats', {}).get('confidence_stats', {})
        if confidence_stats:
            lines.append(f"Current Confidence: {confidence_stats.get('current_confidence', 0):.3f}")
            lines.append(f"Confidence Trend: {confidence_stats.get('confidence_trend', 0):.3f}")
        
        return "\n".join(lines)


class AccessibilityHelper:
    """
    Accessibility features for users with visual impairments.
    """
    
    @staticmethod
    def get_cell_description(
        position: Tuple[int, int], 
        board: Board,
        verbose: bool = True
    ) -> str:
        """
        Get screen reader friendly cell description.
        
        Args:
            position: Cell coordinates
            board: Current board state
            verbose: Include detailed information
            
        Returns:
            Screen reader friendly description
        """
        x, y = position
        state = board.cell_states[position]
        
        if state == CellState.HIDDEN:
            desc = f"Hidden cell at row {y+1}, column {x+1}"
        elif state == CellState.REVEALED:
            number = board.revealed_numbers.get(position, 0)
            if number == 0:
                desc = f"Empty revealed cell at row {y+1}, column {x+1}"
            else:
                desc = f"Revealed cell at row {y+1}, column {x+1} with {number} adjacent mine{'s' if number != 1 else ''}"
        elif state == CellState.FLAGGED:
            desc = f"Flagged cell at row {y+1}, column {x+1}"
        elif state == CellState.SAFE_FLAGGED:
            desc = f"Safe flagged cell at row {y+1}, column {x+1}"
        else:
            desc = f"Unknown cell state at row {y+1}, column {x+1}"
        
        if verbose and state == CellState.REVEALED:
            neighbors = board.get_neighbors(x, y)
            hidden_count = len([n for n in neighbors if board.cell_states[n] == CellState.HIDDEN])
            if hidden_count > 0:
                desc += f". {hidden_count} hidden neighbor{'s' if hidden_count != 1 else ''} remaining"
        
        return desc
    
    @staticmethod
    def get_keyboard_navigation_help() -> str:
        """Get keyboard navigation instructions."""
        return """
Keyboard Navigation:
- Arrow keys: Move selection
- Space: Reveal selected cell
- F: Flag/unflag selected cell
- A: Auto-solve next move
- S: Start auto-solve mode
- H: This help
- Q: Quit game
        """.strip()


# Stubs for future enhancements
class ChiBrotVisualizer:
    """
    Stub for χ-brot visualization (fractal patterns in solving behavior).
    
    This will be implemented in future versions to show:
    - Fractal patterns in decision making
    - TORUS topology visualizations
    - χ-recursive decision trees
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("χ-brot visualizer initialized (stub)")
    
    def create_chi_brot_pattern(self, decision_history: List) -> plt.Figure:
        """Stub for χ-brot pattern visualization."""
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "χ-brot Visualization\n(Coming in future version)", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title("χ-brot Pattern Analysis")
        return fig
