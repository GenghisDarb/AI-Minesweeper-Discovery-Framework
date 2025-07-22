import json
import tempfile

import streamlit as st

from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.ui_widgets import (
    apply_grid_styling,
    color_coded_cell_rendering,
    render_unresolved_hypotheses,
    update_hypotheses_panel,
)
from ai_minesweeper.torus_recursion.dpp14_recursion_engine import DPP14RecursionEngine


def main():
    st.title("AI Minesweeper Discovery Framework")

    # Initialize session state variables
    if "board" not in st.session_state:
        st.session_state.board = None
    if "solver" not in st.session_state:
        st.session_state.solver = None
    if "beta_confidence" not in st.session_state:
        st.session_state.beta_confidence = BetaConfidence()
    if "revealed_hypotheses" not in st.session_state:
        st.session_state.revealed_hypotheses = []
    if "solver_paused" not in st.session_state:
        st.session_state.solver_paused = True
    if "confidence_history" not in st.session_state:
        st.session_state.confidence_history = []

    # Define toggles for execution modes
    step_by_step = st.sidebar.checkbox("Step-by-step mode", value=True)
    auto_discover = st.sidebar.checkbox("Auto-discover (run continuously)", value=False)

    # Upload CSV board
    csv_file = st.file_uploader("Upload a CSV board", type=["csv"])

    if csv_file:
        board = BoardBuilder.from_csv(csv_file)
        st.session_state.board = board  # Persist board in session state
        st.write("Initial Board State:")
        for row in board.grid:
            st.write([color_coded_cell_rendering(cell.state.name) for cell in row])

        # Initialize solver in session state
        if not st.session_state.solver:
            st.session_state.solver = RiskAssessor()

        # Apply grid styling and accessibility features at app start
        apply_grid_styling()

    # Auto-discover mode logic
    def _as_coords(move):
        return move if isinstance(move, tuple) else (move.row, move.col)

    if auto_discover and st.session_state.board and st.session_state.solver:
        tau = st.session_state.beta_confidence.get_threshold()
        while not st.session_state.board.is_solved():
            move = st.session_state.solver.choose_move(st.session_state.board)
            if move is None:
                st.write("No moves left or board solved.")
                break
            risk_map = st.session_state.solver.estimate(st.session_state.board)
            # Sanitize risk_map: coerce None/non-numeric to 1.0 after normalization
            for k in risk_map:
                if risk_map[k] is None or not isinstance(risk_map[k], (int, float)):
                    risk_map[k] = 1.0
            coords = _as_coords(move)
            risk = risk_map.get(coords, 1.0)
            # Fallback: coerce None or invalid risk to 1.0
            if risk is None or not isinstance(risk, (int, float)):
                risk = 1.0
            if hasattr(st.session_state.board, "grid"):
                cell = st.session_state.board.grid[coords[0]][coords[1]]
            else:
                # Fallback for mocks
                cell = move if not isinstance(move, tuple) else None
            if risk > tau:
                st.write("Stopping auto-play: Risk exceeds threshold.")
                break
            if hasattr(st.session_state.board, "reveal") and cell is not None:
                st.session_state.board.reveal(cell)
            st.session_state.beta_confidence.update(
                predicted_probability=risk, revealed_is_mine=getattr(cell, 'is_mine', False) if cell is not None else False
            )
            # Record confidence history
            st.session_state.confidence_history.append(st.session_state.beta_confidence.mean())
            # Live plot of confidence oscillations
            st.line_chart(st.session_state.confidence_history)

    # Update revealed hypotheses logic
    if st.session_state.revealed_hypotheses:
        st.sidebar.markdown("### Revealed Hypotheses")
        for cell in st.session_state.revealed_hypotheses:
            label = cell.description or 'Hypothesis'
            st.sidebar.write(f"({cell.row}, {cell.col}) – {label}: **{cell.state.name}**")

    # Finish session button
    if st.button("Finish Session"):
        st.write("Session ended by user.")
        return

    # Modify end condition logic
    if st.session_state.board and st.session_state.board.is_solved():
        st.write("All hypotheses resolved. Discovery complete!")
        return

    # Confidence History & τ Trajectory Visualization
    if "confidence_history" not in st.session_state:
        st.session_state.confidence_history = []

    # Initialize BetaConfidence instance
    if "beta_confidence" not in st.session_state:
        st.session_state.beta_confidence = BetaConfidence()

    # Update confidence dynamically
    current_confidence = st.session_state.beta_confidence.mean()
    st.metric("Solver Confidence", f"{current_confidence:.2%}")
    st.progress(current_confidence)
    # Append and visualize at session end
    st.session_state.confidence_history.append(current_confidence)
    st.area_chart(st.session_state.confidence_history)

    # Add DPP14 Recursion Engine execution
    if st.button("Run DPP14 Recursion Engine"):
        if st.session_state.board:
            engine = DPP14RecursionEngine(
                board=st.session_state.board,
                solver_policy_class=RiskAssessor,
                debug_mode=True,
            )
            results = engine.run()
            st.write("DPP14 Recursion Engine Results:")
            st.json(results)
        else:
            st.warning("Please upload a board before running the engine.")


if __name__ == "__main__":
    main()
