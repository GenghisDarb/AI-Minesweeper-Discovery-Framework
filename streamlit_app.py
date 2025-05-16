"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor

# --- Sidebar controls ---
st.sidebar.title("Board Controls")

# Board size selector
size = st.sidebar.selectbox("Board size", ["5x5", "9x9", "16x16"], index=1)
size_map = {"5x5": (5, 5), "9x9": (9, 9), "16x16": (16, 16)}

# File uploader
uploaded = st.sidebar.file_uploader("Load board (CSV or ASCII)", type=["csv", "txt"])

# Reset button
if st.sidebar.button("Reset board"):
    st.session_state.clear()
    st.experimental_rerun()

def load_board():
    if uploaded:
        content = uploaded.read().decode()
        if uploaded.name.endswith(".csv"):
            board = BoardBuilder.from_csv(uploaded).build()
        else:
            board = BoardBuilder.from_ascii(content).build()
    else:
        # Default: blank board of selected size
        rows, cols = size_map[size]
        ascii_board = "\n".join(["." * cols for _ in range(rows)])
        board = BoardBuilder.from_ascii(ascii_board).build()
    return board

if "board" not in st.session_state:
    st.session_state.board = load_board()
    st.session_state.assessor = RiskAssessor(st.session_state.board)
    st.session_state.moves = []
    st.session_state.mines_left = getattr(st.session_state.board, "n_mines", 10)

# ---------- helpers ----------------------------------------------------------
def init_state() -> None:
    board = BoardBuilder.from_csv("examples/boards/mini.csv").build()
    st.session_state.board = board
    st.session_state.assessor = RiskAssessor(board)
    st.session_state.moves: list[tuple[int, int]] = []
    st.session_state.mines_left = board.n_mines


@st.cache_data(ttl=0)
def cached_probs(board):
    return RiskAssessor(board).compute_probabilities()


def draw_board(board, probs):
    for r in range(board.n_rows):
        cols = st.columns(board.n_cols, gap="small")
        for c in range(board.n_cols):
            cell = board.grid[r][c]
            key = f"{r}-{c}"
            prob = probs.get((r, c), 0.0)
            if cell.state.name == "REVEALED":
                label = str(getattr(cell, "clue", "")) if not getattr(cell, "is_mine", False) else "💣"
            elif getattr(cell, "is_mine", False):
                label = "💣"
            else:
                label = "⬜"
            if st.button(label, key=key, help=f"Mine risk: {prob:.0%}"):
                if cell.state.name != "REVEALED":
                    cell.state = cell.state.REVEALED
                    st.session_state.moves.append((r, c))
                    if getattr(cell, "is_mine", False):
                        st.session_state.mines_left -= 1
            cols[c].markdown(f"{label}<br>…")


# ---------- Streamlit app ----------------------------------------------------
def main() -> None:
    if "board" not in st.session_state:
        init_state()

    board = st.session_state.board
    assessor: RiskAssessor = st.session_state.assessor
    probs = cached_probs(board)

    st.title("AI-Minesweeper • Hybrid Risk Demo")
    draw_board(board, probs)

    if st.button("Solver move"):
        r, c = assessor.choose_move()
        cell = st.session_state.board.grid[r][c]
        if cell.state.name != "REVEALED":
            cell.state = cell.state.REVEALED
            st.session_state.moves.append((r, c))
            if getattr(cell, "is_mine", False):
                st.session_state.mines_left -= 1
        st.session_state.assessor = RiskAssessor(st.session_state.board)
        st.experimental_rerun()

    if st.session_state.mines_left == 0:
        st.balloons()
        st.success("All mines found! 🎉")

    st.sidebar.write(f"**Moves taken:** {len(st.session_state.moves)}")
    st.sidebar.write(f"**Mines left:** {st.session_state.mines_left}")


if __name__ == "__main__":
    main()

