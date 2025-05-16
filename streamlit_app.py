"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor

# ---------- helpers ----------------------------------------------------------
def init_state() -> None:
    board = BoardBuilder.from_csv("examples/boards/mini.csv").build()
    st.session_state.board = board
    st.session_state.assessor = RiskAssessor(board)
    st.session_state.moves: list[tuple[int, int]] = []
    st.session_state.mines_left = board.n_mines


def draw_board(board, probs) -> None:
    for r in range(board.n_rows):
        cols = st.columns(board.n_cols, gap="small")
        for c in range(board.n_cols):
            cell = board.grid[r][c]
            label = cell.char if cell.state.name == "REVEALED" else "⬜"
            prob = probs.get((r, c), 0.0)
            cols[c].markdown(
                f"{label}<br><span style='font-size:0.75em'>{prob:.0%}</span>",
                unsafe_allow_html=True,
            )


# ---------- Streamlit app ----------------------------------------------------
def main() -> None:
    if "board" not in st.session_state:
        init_state()

    board = st.session_state.board
    assessor: RiskAssessor = st.session_state.assessor
    probs = assessor.compute_probabilities()

    st.title("AI-Minesweeper • Hybrid Risk Demo")
    draw_board(board, probs)

    if st.button("Next move"):
        r, c = assessor.choose_move()
        st.session_state.moves.append((r, c))
        board.grid[r][c].state = board.grid[r][c].state.REVEALED
        st.session_state.assessor = RiskAssessor(board)
        st.experimental_rerun()

    st.sidebar.write(f"**Moves taken:** {len(st.session_state.moves)}")
    st.sidebar.write(f"**Mines left:** {st.session_state.mines_left}")


if __name__ == "__main__":
    main()

[project.optional-dependencies.dev]
streamlit = "^1.35.0"
