# ruff: noqa: I001
import logging
from typing import Any

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
# Streamlit import with safe fallback for headless test environments
try:  # pragma: no cover - import guard
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover - headless CI fallback
    class _StubStreamlit:
        def markdown(self, *args, **kwargs):
            return None

        def write(self, *args, **kwargs):
            return None

        def button(self, *args, **kwargs):
            return False

        def progress(self, *args, **kwargs):
            return None

        def subheader(self, *args, **kwargs):
            return None

        def text_input(self, *args, **kwargs):
            return ""

        def text_area(self, *args, **kwargs):
            return ""

        def columns(self, n: int):
            return [self for _ in range(n)]

        def caption(self, *args, **kwargs):
            return None

        def warning(self, *args, **kwargs):
            return None

        def info(self, *args, **kwargs):
            return None

        def success(self, *args, **kwargs):
            return None

    st = _StubStreamlit()  # type: ignore

from .board import Board, CellState
from .constants import CHI_STR6

# Define logger at module scope
logger = logging.getLogger(__name__)

"""
UI Widgets and helpers for AI Minesweeper visualization.

This module provides UI components for:
- Color-coding and visual styling
- Tooltips and accessibility features
- χ-cycle visualization
- High-contrast mode support
- TORUS theory visualization stubs
"""


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
            8: "#808080",
        },
        "confidence_low": "#FFE5E5",
        "confidence_medium": "#FFF5E5",
        "confidence_high": "#E5F5E5",
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
            8: "#808080",
        },
        "confidence_low": "#330000",
        "confidence_medium": "#333300",
        "confidence_high": "#003300",
    }

    # χ-cycle visualization colors
    CHI_CYCLE = {
        "phase_0": "#FF6B6B",
        "phase_1": "#4ECDC4",
        "phase_2": "#45B7D1",
        "phase_3": "#96CEB4",
        "phase_4": "#FECA57",
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
        self.color_scheme = (
            ColorScheme.HIGH_CONTRAST
            if high_contrast
            else ColorScheme.DEFAULT
        )
        self.logger = logging.getLogger(__name__)

        # Set up matplotlib style
        plt.style.use(
            "seaborn-v0_8" if hasattr(plt.style, "seaborn-v0_8") else "default"
        )

    def create_board_visualization(
        self,
        board: Board,
        risk_map: dict[tuple[int, int], float] | None = None,
        confidence_overlay: bool = False,
    ) -> Any:
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
        w = int(getattr(board, 'width', getattr(board, 'n_cols', 0)) or 0)
        h = int(getattr(board, 'height', getattr(board, 'n_rows', 0)) or 0)
        ax.set_xlim(-0.5, w - 0.5)
        ax.set_ylim(-0.5, h - 0.5)
        ax.set_aspect("equal")
        ax.invert_yaxis()  # Standard minesweeper layout

        # Remove tick marks
        ax.set_xticks(range(w))
        ax.set_yticks(range(h))
        ax.grid(True, alpha=0.3)

        # Title with game state
        title = f"AI Minesweeper {getattr(board,'width', w)}x{getattr(board,'height', h)} - Mines: {getattr(board,'remaining_mines',0)}/{getattr(board,'mine_count',0)}"
        if hasattr(board, 'is_solved') and callable(board.is_solved) and board.is_solved():
            title += " ✅ SOLVED"
        ax.set_title(title, fontsize=14, fontweight="bold")

        return fig

    @staticmethod
    def sidebar_constants() -> dict:
        """Small adapter exposing constants expected by UI/tests."""
        return {"χ": CHI_STR6}

    def _draw_board_grid(
        self,
        ax: Any,
        board: Board,
        risk_map: dict[tuple[int, int], float] | None,
        confidence_overlay: bool,
    ) -> None:
        """Draw the basic board grid with cell backgrounds."""
        w = int(getattr(board, 'width', getattr(board, 'n_cols', 0)) or 0)
        h = int(getattr(board, 'height', getattr(board, 'n_rows', 0)) or 0)
        for x in range(w):
            for y in range(h):
                pos = (x, y)
                state = board.cell_states[pos]

                # Determine cell color
                if confidence_overlay and risk_map and pos in risk_map:
                    color = self._get_confidence_color(risk_map[pos])
                else:
                    color = self._get_cell_color(state)

                # Draw cell rectangle
                rect = patches.Rectangle(
                    (x - 0.4, y - 0.4),
                    0.8,
                    0.8,
                    linewidth=1,
                    edgecolor="black",
                    facecolor=color,
                )
                ax.add_patch(rect)

    def _draw_cell_contents(self, ax: Any, board: Board) -> None:
        """Draw cell contents (numbers, flags, mines)."""
        w = int(getattr(board, 'width', getattr(board, 'n_cols', 0)) or 0)
        h = int(getattr(board, 'height', getattr(board, 'n_rows', 0)) or 0)
        for x in range(w):
            for y in range(h):
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
                    ax.text(
                        x,
                        y,
                        text,
                        ha="center",
                        va="center",
                        fontsize=12,
                        fontweight="bold",
                        color=text_color,
                    )

    def _draw_risk_overlay(
        self,
        ax: Any,
        board: Board,
        risk_map: dict[tuple[int, int], float],
    ) -> None:
        """Draw risk assessment overlay."""
        # Create risk heatmap
        w = int(getattr(board, 'width', getattr(board, 'n_cols', 0)) or 0)
        h = int(getattr(board, 'height', getattr(board, 'n_rows', 0)) or 0)
        risk_data = np.zeros((h, w))
        for (x, y), risk in risk_map.items():
            risk_data[y, x] = risk

        # Create transparent overlay
        im = ax.imshow(risk_data, cmap="Reds", alpha=0.3, vmin=0, vmax=1)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label("Mine Risk", rotation=270, labelpad=15)

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
        self, confidence_history: list[float], chi_cycle_count: int
    ) -> Any:
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
            ax1.plot(x_vals, confidence_history, "b-", linewidth=2, label="Confidence")

            # Add trend line
            if len(confidence_history) > 3:
                z = np.polyfit(x_vals, confidence_history, 1)
                p = np.poly1d(z)
                ax1.plot(x_vals, p(x_vals), "r--", alpha=0.7, label="Trend")

            ax1.set_ylabel("Confidence Level")
            ax1.set_title("χ-Recursive Confidence Evolution")
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 1)

        # χ-cycle phase visualization
        phase = (chi_cycle_count % 20) / 20.0
        phases = np.linspace(0, 2 * np.pi, 100)
        cycle_signal = 0.5 + 0.5 * np.sin(phases)

        ax2.plot(phases, cycle_signal, "g-", linewidth=2, label="χ-Cycle")
        current_phase = 2 * np.pi * phase
        current_value = 0.5 + 0.5 * np.sin(current_phase)
        ax2.plot(current_phase, current_value, "ro", markersize=10, label="Current Phase")

        ax2.set_xlabel("Phase (radians)")
        ax2.set_ylabel("Cycle Value")
        ax2.set_title(f"TORUS Theory χ-Cycle (Count: {chi_cycle_count})")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def create_risk_distribution_plot(
        self, risk_map: dict[tuple[int, int], float]
    ) -> Any:
        """
        Create risk distribution analysis plot.

        Args:
            risk_map: Risk assessment data

        Returns:
            Matplotlib figure with risk analysis
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        if not risk_map:
            ax1.text(0.5, 0.5, "No risk data available", ha="center", va="center")
            ax2.text(0.5, 0.5, "No risk data available", ha="center", va="center")
            return fig

        risks = list(risk_map.values())

        # Risk histogram
        ax1.hist(risks, bins=20, alpha=0.7, color="skyblue", edgecolor="black")
        ax1.set_xlabel("Risk Level")
        ax1.set_ylabel("Number of Cells")
        ax1.set_title("Risk Distribution")
        ax1.grid(True, alpha=0.3)

        # Risk categories
        safe_count = len([r for r in risks if r < 0.2])
        medium_count = len([r for r in risks if 0.2 <= r < 0.8])
        danger_count = len([r for r in risks if r >= 0.8])

        categories = ["Safe\n(<0.2)", "Medium\n(0.2-0.8)", "Dangerous\n(≥0.8)"]
        counts = [safe_count, medium_count, danger_count]
        colors = ["green", "orange", "red"]

        ax2.bar(categories, counts, color=colors, alpha=0.7)
        ax2.set_ylabel("Number of Cells")
        ax2.set_title("Risk Categories")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


class TooltipManager:
    """
    Tooltip and accessibility manager for interactive UI components.
    """

    def __init__(self):
        """Initialize tooltip manager."""
        self.active_tooltips: dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)

    def create_cell_tooltip(
        self,
        position: tuple[int, int],
        board: Board,
        risk: float | None = None,
        confidence: float | None = None,
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
            hidden_neighbors = len(
                [n for n in neighbors if board.cell_states[n] == CellState.HIDDEN]
            )
            flagged_neighbors = len(
                [
                    n
                    for n in neighbors
                    if board.cell_states[n]
                    in [CellState.FLAGGED, CellState.SAFE_FLAGGED]
                ]
            )

            tooltip_lines.append(f"Hidden neighbors: {hidden_neighbors}")
            tooltip_lines.append(f"Flagged neighbors: {flagged_neighbors}")

        return "\n".join(tooltip_lines)

    def create_solver_status_tooltip(self, solver_stats: dict) -> str:
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

        confidence_stats = solver_stats.get("policy_stats", {}).get("confidence_stats", {})
        if confidence_stats:
            lines.append(
                f"Current Confidence: {confidence_stats.get('current_confidence', 0):.3f}"
            )
            lines.append(
                f"Confidence Trend: {confidence_stats.get('confidence_trend', 0):.3f}"
            )

        return "\n".join(lines)


class AccessibilityHelper:
    """
    Accessibility features for users with visual impairments.
    """

    @staticmethod
    def get_cell_description(
        position: tuple[int, int],
        board: Board,
        verbose: bool = True,
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

    def create_chi_brot_pattern(self, decision_history: list) -> Any:
        """Stub for χ-brot pattern visualization."""
        fig, ax = plt.subplots()
        ax.text(
            0.5,
            0.5,
            "χ-brot Visualization\n(Coming in future version)",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        ax.set_title("χ-brot Pattern Analysis")
        return fig


def display_confidence(confidence: float, mode: str = "cli") -> str:
    """Display confidence level in different modes."""
    if mode == "cli":
        return f"Confidence: {confidence * 100:.1f}%"
    elif mode == "ui":
        # Placeholder for UI rendering logic
        return f"Confidence displayed in UI: {confidence * 100:.1f}%"
    else:
        raise ValueError("Unsupported mode. Use 'cli' or 'ui'.")

def add_accessibility_labels_to_cells(board: Board) -> None:
    """Add simple ARIA-like labels on cells for screen readers.

    This function attaches a "aria_label" attribute to each cell with a
    deterministic description string. Safe for tests and headless use.
    """
    logger.info("Adding accessibility labels to cells.")
    try:
        for y in range(getattr(board, 'height', getattr(board, 'n_rows', 0)) or 0):
            for x in range(getattr(board, 'width', getattr(board, 'n_cols', 0)) or 0):
                pos = (x, y)
                state = board.cell_states.get(pos)
                if state is None:
                    continue
                # Minimal, deterministic label
                label = f"cell r{y+1} c{x+1} state {getattr(state, 'name', str(state))}"
                # Attach to board if per-cell object exists; else store in a dict
                cell_obj = None
                try:
                    cell_obj = board.grid[y][x]
                except Exception:
                    cell_obj = None
                if cell_obj is not None:
                    try:
                        cell_obj.aria_label = label  # type: ignore[attr-defined]
                    except Exception:
                    except Exception as e:
                        logger.debug(f"Failed to set aria_label on cell_obj at ({x}, {y}): {e}", exc_info=True)
                else:
                    # Fallback storage
                    if not hasattr(board, "_aria_labels"):
                        try:
                            board._aria_labels = {}  # type: ignore[attr-defined]
                        except Exception:
                            return
                    board._aria_labels[pos] = label  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - defensive
        logger.debug("Accessibility labels skipped (board structure mismatch)")

def add_high_contrast_mode(board: Board | None = None) -> None:
    """Enable high-contrast mode for the board."""
    logger.info("Enabling high-contrast mode.")
    # Apply high-contrast CSS class
    st.markdown('<div class="high-contrast">', unsafe_allow_html=True)
    # Render the board here
    st.markdown('</div>', unsafe_allow_html=True)

def add_colorblind_friendly_palette(board: Board) -> None:
    """Enable colorblind-friendly palette for the board."""
    logger.info("Enabling colorblind-friendly palette.")
    # Apply colorblind-friendly CSS class
    st.markdown('<div class="colorblind-friendly">', unsafe_allow_html=True)
    # Render the board here
    st.markdown('</div>', unsafe_allow_html=True)

def add_chat_interface_placeholder() -> None:
    """Render a disabled chat input with explicit 'LLM disabled' banner."""
    st.warning("LLM disabled. Set AIMS_LLM_PROVIDER=openai and provide OPENAI_API_KEY to enable.")
    st.text_input(
        "Ask the AI assistant:",
        disabled=True,
        help="Provide credentials and provider to enable deterministic LLM assist."
    )

def align_chat_input_with_ui() -> None:
    """
    Apply minimal CSS so the chat input aligns with surrounding UI elements.
    Safe in headless mode; no-ops if Streamlit is stubbed.
    """
    st.markdown(
        """
        <style>
            .stTextInput > div > div > input {
                max-width: 640px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def rank_hypotheses_core(hyps: list[str]) -> list[str]:
    """Pure deterministic baseline ranking for hypotheses.

    Stable key ensures reproducible ordering independent of platform locale.
    """
    return sorted(hyps or [], key=lambda s: (len(s), s))

def render_llm_chat(hypotheses: list[str] | None = None) -> list[str] | None:
    """Render a minimal chat/ranking UI for hypotheses with deterministic fallback.

    Behavior:
    - If hypotheses are provided, they will be pre-filled in the textarea (one per line).
    - If not provided, the user can paste hypotheses manually.
    - Clicking "Rank" calls llm_suggest with temperature=0 provider settings via llm_interface,
      which will deterministically fall back when config/keys are missing.

    Returns:
    - Ranked list when available, else None.
    """
    try:
        from .llm_interface import llm_suggest
    except Exception:
        llm_suggest = None  # type: ignore

    st.subheader("AI Assistant (Hypothesis Ranking)")
    default_text = "\n".join(hypotheses) if hypotheses else ""
    text = st.text_area(
        "Enter hypotheses (one per line):",
        value=default_text,
        height=150,
        help="The assistant will re-order only; no new items will be added.",
    )

    # Render controls (avoid context managers to keep headless stub simple)
    do_rank = st.button("Rank", type="primary")
    st.caption("Deterministic: temperature=0; safe fallback if LLM unavailable.")

    if not do_rank:
        return None

    items = [s.strip() for s in text.splitlines() if s.strip()]
    if not items:
        st.info("Provide at least one hypothesis to rank.")
        return None

    ranked_list: list[str]
    if llm_suggest is None:
        st.warning("LLM interface unavailable; using deterministic baseline ordering.")
        ranked_list = rank_hypotheses_core(items)
    else:
        try:
            # Provider expects a snapshot; for ranking, we only pass the list
            # under a neutral key. The provider may ignore this and UI will still
            # deterministically fall back.
            suggestions = llm_suggest({"hypotheses": items})  # type: ignore[arg-type]
            # If provider returns structured suggestions with 'text', use them; else fallback
            extracted: list[str] = [
                str(s.get("text"))
                for s in suggestions
                if isinstance(s, dict) and isinstance(s.get("text"), str)
            ]
            ranked_list = extracted if extracted else rank_hypotheses_core(items)
        except Exception as ex:  # pragma: no cover - defensive UI path
            logger.warning("llm_suggest failed: %s", ex)
            st.warning("LLM failed; using deterministic baseline ordering.")
            ranked_list = rank_hypotheses_core(items)

    st.success("Ranking complete.")
    for i, h in enumerate(ranked_list, 1):
        st.write(f"{i}. {h}")
    return ranked_list

def apply_grid_styling() -> None:
        """Apply consistent grid styling (high-contrast borders, readable fonts)."""
        st.markdown(
                """
                <style>
                    .grid { border-collapse: collapse; }
                    .grid td, .grid th { border: 1px solid #333; padding: 4px; }
                    .cell-hidden { background: #C0C0C0; }
                    .cell-revealed { background: #F0F0F0; }
                    .cell-flagged { background: #FF6B6B; }
                </style>
                """,
                unsafe_allow_html=True,
        )

def ensure_grid_styling_consistency():
    """
    Ensure consistent grid styling by applying a uniform CSS class to the grid.
    """
    logger.info("Ensuring grid styling consistency.")
    st.markdown('<style>.grid { border-collapse: collapse; }</style>', unsafe_allow_html=True)

def ensure_persistent_unexplored_cells(board: Board):
    """
    Ensure unexplored cells remain visually distinct on the board.
    """
    logger.info("Ensuring persistent unexplored cells.")
    for row in getattr(board, 'grid', []):
        for cell in row:
            if hasattr(cell, 'state') and cell.state == CellState.HIDDEN:
                cell.style = "background-color: lightgray;"


def chi_brot_visualization(board: Board | None = None) -> str:
    """Render a deterministic χ-brot style preview and save to artifacts/chi_brot.png.

    Uses headless Agg backend and a simple parametric curve whose phase is driven by
    an integer chi-cycle counter if present on the board (else 0).

    Returns the output file path.
    """
    # Force Agg backend for headless stability in CI
    try:  # local import to avoid global backend mutation
        import matplotlib
        matplotlib.use("Agg", force=True)
    except Exception:
        pass

    # Derive a deterministic phase from board
    chi = 0
    try:
        # Support various attribute names used in code/tests
        for attr in ("chi_cycle_count", "chi_cycle", "chi", "chi_phase", "cycle"):
            if hasattr(board, attr):
                chi = int(getattr(board, attr) or 0)
                break
    except Exception:
        chi = 0

    # Parametric curve: small Lissajous with chi-based phase
    t = np.linspace(0, 2 * np.pi, 400)
    a, b = 3, 2
    delta = (chi % 20) * (np.pi / 10.0)
    x = np.cos(a * t + delta)
    y = np.sin(b * t)

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.plot(x, y, color="#3366cc", linewidth=1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"χ-brot preview (χ={chi})", fontsize=9)
    ax.set_aspect("equal")
    ax.grid(False)

    # Ensure output dir
    import os
    out_dir = os.path.join(os.getcwd(), "artifacts")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "chi_brot.png")
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out_path

def highlight_newly_revealed_cells(board: Board):
    """
    Highlight cells that were revealed in the last move.
    """
    logger.info("Highlighting newly revealed cells.")
    for row in getattr(board, 'grid', []):
        for cell in row:
            if hasattr(cell, 'state') and cell.state == CellState.REVEALED and getattr(cell, 'recently_revealed', False):
                cell.style = "background-color: yellow;"

def highlight_zero_value_reveals(board: Board, revealed_cells: list[Any] | None = None):
    """
    Highlight cells with zero adjacent mines when revealed.
    """
    logger.info("Highlighting zero-value reveals.")
    # If explicit cells provided (tests), mark them and return
    if revealed_cells is not None:
        for cell in revealed_cells:
            try:
                cell.style = "background-color: green;"
            except Exception:
                pass
        return
    # Otherwise operate on the board grid
    for row in getattr(board, 'grid', []):
        for cell in row:
            if hasattr(cell, 'state') and cell.state == CellState.REVEALED and getattr(cell, 'clue', None) == 0:
                cell.style = "background-color: green;"

def render_cell_with_tooltip(*args, **kwargs):
    """Two modes:
    - Called as (state: str, message: str) -> returns HTML string (for unit tests)
    - Called as (board: Board) -> renders tooltips for each cell via Streamlit
    """
    if len(args) >= 2 and isinstance(args[0], str):
        state, message = args[0], args[1]
        color = "green" if state == "safe" else ("red" if state == "mine" else "gray")
        html = f'<div style="background-color: {color}; padding: 4px;" title="{message}">{message}</div>'
        return html
    # Board rendering path
    board: Board | None = args[0] if args else kwargs.get('board')
    logger.info("Rendering cells with tooltips.")
    if board is None:
        return ""
    for row in getattr(board, 'grid', []):
        for cell in row:
            if not hasattr(cell, 'row') or not hasattr(cell, 'col') or not hasattr(cell, 'state'):
                continue
            tooltip = f"Row: {getattr(cell,'row',-1)}, Col: {getattr(cell,'col',-1)}, State: {getattr(getattr(cell,'state',None),'name','?')}"
            if getattr(cell, 'state', None) == CellState.REVEALED:
                tooltip += f", Clue: {getattr(cell,'clue','?')}"
            st.markdown(f'<div title="{tooltip}">{getattr(cell, "symbol", "")}</div>', unsafe_allow_html=True)

def render_hypotheses_with_tooltips(board: Board):
    """Render a simple, deterministic hypotheses panel with tooltips.

    Behavior:
    - If board exposes `get_revealed_hypotheses()` -> use it; else, try `hypotheses` attr.
    - Renders each hypothesis with a title tooltip; sorted deterministically by (len, text).
    - No exceptions are raised if nothing is available.
    """
    logger.info("Rendering hypotheses with tooltips.")
    hyps: list[str] = []
    try:
        func = getattr(board, "get_revealed_hypotheses", None)
        if callable(func):
            val = func()
            if isinstance(val, list):
                hyps = [str(x) for x in val]
        elif hasattr(board, "hypotheses") and isinstance(board.hypotheses, list):  # type: ignore[attr-defined]
            hyps = [str(x) for x in board.hypotheses]  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - defensive
        hyps = []

    if not hyps:
        st.info("No hypotheses to display.")
        return

    ordered = sorted(hyps, key=lambda s: (len(s), s))
    st.subheader("Hypotheses")
    for h in ordered:
        st.markdown(f'<div title="{h}">• {h}</div>', unsafe_allow_html=True)

def update_hypotheses_panel(board: Board):
    """Update the hypotheses panel in a deterministic, no-throw way.

    Delegates to `render_hypotheses_with_tooltips` and adds a stable caption.
    """
    logger.info("Updating hypotheses panel.")
    render_hypotheses_with_tooltips(board)
    st.caption("Sorted deterministically by length, then lexicographically.")
