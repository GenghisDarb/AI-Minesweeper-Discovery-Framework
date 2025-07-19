import streamlit as st
from src.ai_minesweeper.ui_widgets import display_confidence, color_coded_cell_rendering, copy_results_button
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
import json
import tempfile

def main():
    st.title("AI Minesweeper Discovery Framework")

    # Upload CSV board
    csv_file = st.file_uploader("Upload a CSV board", type=["csv"])

    if csv_file:
        board = BoardBuilder.from_csv(csv_file)
        st.write("Initial Board State:")
        st.write(board)

        # Step-by-step mode toggle
        step_by_step = st.checkbox("Step-by-step mode", value=True)

        # Auto-discover toggle
        auto_discover = st.sidebar.checkbox("Auto-discover mode", value=False)
        st.session_state.auto_discover = auto_discover

        # Revealed Hypotheses Summary Panel
        revealed_hypotheses = []

        # Initialize session state for solver pause
        if "solver_paused" not in st.session_state:
            st.session_state.solver_paused = True

        # Initialize session state for solver and revealed_hypotheses
        if "solver" not in st.session_state:
            st.session_state["solver"] = None

        if "revealed_hypotheses" not in st.session_state:
            st.session_state["revealed_hypotheses"] = []

        if st.button("Start Discovery"):
            solver = RiskAssessor()

            # Main loop logic for step-by-step mode
            if not st.session_state.solver_paused or auto_discover:
                solver.step(board)  # Removed unused variable 'result'
                if not auto_discover:
                    st.session_state.solver_paused = True

            if auto_discover:
                while not board.is_solved():
                    move = solver.choose_move(board)
                    board.reveal(move)
                    st.write(board)
            else:
                move = solver.choose_move(board)
                board.reveal(move)
                st.write(board)

        # Solver Move button for step-by-step mode
        if step_by_step:
            # Add button to trigger a solver step
            if st.button("🔍 Solver Move (Step)"):
                st.session_state.solver_paused = False

            if not st.session_state.solver_paused:
                solver.step(board)  # Removed unused variable 'result'
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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp_file:
                json.dump(board_state, tmp_file, indent=2)
                tmp_path = tmp_file.name
            st.download_button("Download JSON", tmp_path, file_name="board_state.json")

    # Placeholder for confidence level
    confidence = 0.75  # Example confidence value
    display_confidence(confidence, mode="streamlit")

    # Example board rendering
    st.markdown("### Minesweeper Board")
    board = [
        ["hidden", "safe", "mine"],
        ["clue", "hidden", "safe"],
        ["mine", "clue", "hidden"],
    ]

    for row in board:
        st.markdown(" ".join([color_coded_cell_rendering(cell) for cell in row]), unsafe_allow_html=True)

    # Add a button to copy results
    results = {"board_state": board, "confidence": confidence}
    copy_results_button(results)

    # Chat/Feedback Input Box
    user_feedback = st.text_input("💬 Ask the AI or provide feedback:")
    if user_feedback:
        st.write(f"You said: {user_feedback}")
        # Placeholder for future AI interaction logic

if __name__ == "__main__":
    main()