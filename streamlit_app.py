import json
import tempfile

import streamlit as st

from ai_minesweeper.beta_confidence import BetaConfidence
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.ui_widgets import (
    render_unresolved_hypotheses,
    update_hypotheses_panel,
    apply_grid_styling,
    add_accessibility_labels_to_cells,
    add_colorblind_friendly_palette,
    add_high_contrast_mode,
    color_coded_cell_rendering,
)


def main():
    st.title("AI Minesweeper Discovery Framework")

    # Upload CSV board
    csv_file = st.file_uploader("Upload a CSV board", type=["csv"])

    if csv_file:
        board = BoardBuilder.from_csv(csv_file)
        st.session_state.board = board  # Persist board in session state
        st.write("Initial Board State:")
        for row in board.grid:
            st.write([color_coded_cell_rendering(cell.state.name) for cell in row])

        # Initialize solver in session state
        if "solver" not in st.session_state:
            st.session_state.solver = RiskAssessor()

        # Initialize BetaConfidence and confidence history in session state
        if "beta_confidence" not in st.session_state:
            st.session_state.beta_confidence = BetaConfidence()
        if "confidence_history" not in st.session_state:
            st.session_state.confidence_history = []

        # Apply grid styling and accessibility features at app start
        apply_grid_styling()
        if st.sidebar.checkbox("Enable colorblind-friendly palette"):
            add_colorblind_friendly_palette()
        if st.sidebar.checkbox("Enable high-contrast mode"):
            add_high_contrast_mode()

        # Add accessibility labels to cells
        if "board" in st.session_state:
            add_accessibility_labels_to_cells(st.session_state.board)

        # Step-by-step mode logic
        if step_by_step and st.button("Step Move"):
            cell = st.session_state.solver.choose_move(st.session_state.board)
            predicted_probability = st.session_state.solver.estimate_risk(cell)
            st.session_state.board.reveal(cell)
            st.session_state.beta_confidence.update(
                predicted_probability=predicted_probability, revealed_is_mine=cell.is_mine
            )

            # Append to confidence history and update chart
            current_mean = st.session_state.beta_confidence.mean()
            st.session_state.confidence_history.append(current_mean)
            st.line_chart(st.session_state.confidence_history)

            # Display current confidence
            st.metric("Confidence Level", f"{current_mean * 100:.2f}%")
            st.progress(current_mean)

            # Render unresolved hypotheses and update panel
            render_unresolved_hypotheses(st.session_state.board)
            update_hypotheses_panel(st.session_state.board)

            # Replace inline color rendering with styled div elements
            st.write("Updated Board State:")
            for row in st.session_state.board.grid:
                st.write([color_coded_cell_rendering(cell.state.name) for cell in row])

            # Handle cascade reveals
            if cell.clue == 0:
                cascade_cells = st.session_state.board.get_cascade_cells(cell)
                highlight_zero_value_reveals(cascade_cells)
                st.session_state.revealed_hypotheses.extend(cascade_cells)

        # Auto-discover mode logic
        if auto_discover:
            tau = st.session_state.beta_confidence.get_threshold()
            while not st.session_state.board.is_solved():
                cell = st.session_state.solver.choose_move(st.session_state.board)
                risk = st.session_state.solver.estimate_risk(cell)
                if risk > tau:
                    st.write("Stopping auto-play: Risk exceeds threshold.")
                    break
                st.session_state.board.reveal(cell)
                st.session_state.beta_confidence.update(
                    predicted_probability=risk, revealed_is_mine=cell.is_mine
                )

                # Append to confidence history and update chart
                current_mean = st.session_state.beta_confidence.mean()
                st.session_state.confidence_history.append(current_mean)
                st.line_chart(st.session_state.confidence_history)
            st.write("Final Board State:")
            for row in st.session_state.board.grid:
                st.write([color_coded_cell_rendering(cell.state.name) for cell in row])

        # Solver Move button for step-by-step mode
        if step_by_step:
            # Add button to trigger a solver step
            if st.button("🔍 Solver Move (Step)"):
                st.session_state.solver_paused = False

            if not st.session_state.solver_paused:
                cell = st.session_state.solver.choose_move(st.session_state.board)
                st.session_state.board.reveal(cell)
                st.session_state.beta_confidence.update(
                    predicted_probability=st.session_state.solver.estimate_risk(cell),
                    revealed_is_mine=cell.is_mine
                )

                # Append to confidence history and update chart
                current_mean = st.session_state.beta_confidence.mean()
                st.session_state.confidence_history.append(current_mean)
                st.line_chart(st.session_state.confidence_history)

                # Render unresolved hypotheses and update panel
                render_unresolved_hypotheses(st.session_state.board)
                update_hypotheses_panel(st.session_state.board)

                st.session_state.solver_paused = True

        # Display the summary panel
        if revealed_hypotheses:
            st.sidebar.markdown("### Revealed Hypotheses")
            for cell in revealed_hypotheses:
                st.sidebar.write(f"({cell.row}, {cell.col}) is {cell.state}")

        # Finish session button
        if st.button("Finish Session"):
            st.write("Session ended by user.")
            return

        # Modify end condition logic
        if board.is_solved():
            st.write("All hypotheses resolved. Discovery complete!")
            return

        # Confidence History & τ Trajectory Visualization
        if "confidence_history" not in st.session_state:
            st.session_state.confidence_history = []

        if st.button("Update Confidence History"):
            current_confidence = board.get_current_confidence()
            st.session_state.confidence_history.append(current_confidence)
            st.line_chart(st.session_state.confidence_history)

        # Update Export Board Functionality
        if st.button("Export Board State"):
            board_state = board.export_state()
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".json", mode="w", encoding="utf-8"
            ) as tmp_file:
                json.dump(board_state, tmp_file, indent=2)
                tmp_path = tmp_file.name
            st.download_button("Download JSON", tmp_path, file_name="board_state.json")

    # Initialize BetaConfidence instance
    if "beta_confidence" not in st.session_state:
        st.session_state.beta_confidence = BetaConfidence()

    # Update confidence dynamically
    current_confidence = st.session_state.beta_confidence.mean()
    st.metric("Solver Confidence", f"{current_confidence:.2%}")
    st.progress(current_confidence)

    # Example: Update BetaConfidence based on user input (placeholder logic)
    if st.button("Simulate Confidence Update"):
        st.session_state.beta_confidence.update(success=True)
        st.experimental_rerun()

    # Example board rendering
    st.markdown("### Minesweeper Board")
    board = [
        ["hidden", "safe", "mine"],
        ["clue", "hidden", "safe"],
        ["mine", "clue", "hidden"],
    ]

    for row in board:
        st.markdown(
            " ".join([color_coded_cell_rendering(cell) for cell in row]),
            unsafe_allow_html=True,
        )

    # Define `confidence` before use
    confidence = None

    # Add a button to copy results
    results = {"board_state": board, "confidence": confidence}
    copy_results_button(results)

    # Chat/Feedback Input Box
    user_feedback = st.text_input("💬 Ask the AI or provide feedback:")
    if user_feedback:
        st.write(f"You said: {user_feedback}")
        # Placeholder for future AI interaction logic

    # Revealed Hypotheses Panel
    if "revealed_hypotheses" not in st.session_state:
        st.session_state.revealed_hypotheses = []

    st.sidebar.markdown("### Revealed Hypotheses")
    for cell in st.session_state.revealed_hypotheses:
        st.sidebar.write(f"Cell ({cell.row}, {cell.col})")

    # Highlight newly revealed cells
    def highlight_newly_revealed_cells(revealed_cells):
        for cell in revealed_cells:
            st.write(f"Highlighting cell ({cell.row}, {cell.col})")

    # Cascade reveals
    def highlight_zero_value_reveals(cascade_cells):
        for cell in cascade_cells:
            st.write(f"Cascade reveal for cell ({cell.row}, {cell.col})")

    # Add board export functionality
    if st.button("Export Board as CSV"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            st.session_state.board.to_csv(temp_file.name)
            st.download_button(
                label="Download Board CSV",
                data=open(temp_file.name, "rb").read(),
                file_name="board_state.csv",
                mime="text/csv",
            )

    # Add chat input widget
    user_input = st.text_input("Chat with the AI Minesweeper Assistant:")
    if user_input:
        st.write(f"You said: {user_input}")
        # Placeholder for AI response logic
        st.write("AI Assistant: [Response goes here]")

    # Add dynamic grid expansion controls
    st.sidebar.subheader("Grid Expansion")
    new_rows = st.sidebar.number_input("Add Rows", min_value=0, step=1, value=0)
    new_cols = st.sidebar.number_input("Add Columns", min_value=0, step=1, value=0)

    if st.sidebar.button("Expand Grid"):
        if new_rows > 0 or new_cols > 0:
            st.session_state.board.expand_grid(new_rows, new_cols)
            st.write(f"Grid expanded by {new_rows} rows and {new_cols} columns.")

            # Re-render the updated grid
            st.write("Updated Board State:")
            for row in st.session_state.board.grid:
                st.write([color_coded_cell_rendering(cell.state.name) for cell in row])


if __name__ == "__main__":
    main()
