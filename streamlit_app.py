import streamlit as st
from src.ai_minesweeper.ui_widgets import display_confidence, color_coded_cell_rendering, copy_results_button
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
import json

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
        auto_discover = st.checkbox("Auto-discover")

        # Revealed Hypotheses Summary Panel
        revealed_hypotheses = []

        if st.button("Start Discovery"):
            solver = RiskAssessor()

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
        if step_by_step and st.button("Solver Move"):
            move = solver.choose_move(board)
            revealed_cells = board.reveal(move)
            revealed_hypotheses.extend(revealed_cells)
            st.write(f"Revealed {len(revealed_cells)} new hypotheses:")
            for cell in revealed_cells:
                st.write(f"- ({cell.row}, {cell.col}) is {cell.state}")

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

        # Export Board Functionality
        if st.button("Export Board State"):
            board_state = board.export_state()
            with open("exported_board_state.json", "w") as f:
                json.dump(board_state, f)
            st.success("Board state exported successfully!")

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

    # Confidence History & τ Trajectory
    confidence_history = []

    if st.button("Update Confidence History"):
        confidence_history.append(board.get_current_confidence())
        st.line_chart(confidence_history)

if __name__ == "__main__":
    main()