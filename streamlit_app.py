"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor

# --- Sidebar controls ---
st.sidebar.title("Board Controls")

# File-uploader for CSV or ASCII
uploaded = st.sidebar.file_uploader("Load board (CSV or ASCII)", type=["csv", "txt"])

# Board size dropdown
size = st.sidebar.selectbox("Board size", ["5x5", "9x9", "16x16"], index=1)
size_map = {"5x5": (5, 5), "9x9": (9, 9), "16x16": (16, 16)}

# Reset board on file upload or size change
def reset_board():
    if uploaded:
        content = uploaded.read().decode()
        if uploaded.name.endswith(".csv"):
            board = BoardBuilder.from_csv(uploaded).build()
        else:
            board = BoardBuilder.from_ascii(content).build()
    else:
        rows, cols = size_map[size]
        ascii_board = "\n".join(["." * cols for _ in range(rows)])
        board = BoardBuilder.from_ascii(ascii_board).build()
    st.session_state.board = board
    st.session_state.assessor = RiskAssessor(board)
    st.session_state.moves = []
    st.session_state.mines_left = getattr(board, "n_mines", 10)

# If file uploaded or size changed, reset board
if uploaded or "last_size" not in st.session_state or st.session_state.last_size != size:
    reset_board()
    st.session_state.last_size = size

if st.sidebar.button("Reset board"):
    st.session_state.clear()
    st.experimental_rerun()

def init_state():
    rows, cols = size_map[size]
    ascii_board = "\n".join(["." * cols for _ in range(rows)])
    board = BoardBuilder.from_ascii(ascii_board).build()
    st.session_state.board = board
    st.session_state.assessor = RiskAssessor(board)
    st.session_state.moves = []
    st.session_state.mines_left = getattr(board, "n_mines", 10)

if "board" not in st.session_state:
    init_state()

@st.cache_data(ttl=0)
def cached_probs(board):
    return RiskAssessor(board).compute_probabilities()

def prob_to_rgba(prob):
    # Red for high risk, green for low, alpha for visibility
    r = int(255 * prob)
    g = int(255 * (1 - prob))
    b = 100
    alpha = 0.4 + 0.5 * prob  # more opaque for higher risk
    return f"rgba({r},{g},{b},{alpha:.2f})"

def draw_board(board, probs):
    for r in range(board.n_rows):
        cols = st.columns(board.n_cols, gap="small")
        for c in range(board.n_cols):
            cell = board.grid[r][c]
            key = f"{r}-{c}"
            prob = probs.get((r, c), 0.0)
            bg = prob_to_rgba(prob)
            if cell.state.name == "REVEALED":
                if getattr(cell, "is_mine", False):
                    label = '<span style="font-size:2em;color:#d00;">💣</span>'
                else:
                    clue = getattr(cell, "clue", "")
                    label = f'<span style="font-size:1.5em;color:#06f;">{clue}</span>'
            elif getattr(cell, "is_mine", False):
                label = '<span style="font-size:2em;color:#d00;">💣</span>'
            else:
                label = '<span style="font-size:2em;color:#bbb;">⬜</span>'
            # Clickable cell
            if cols[c].button(" ", key=key, help=f"Mine risk: {prob:.0%}"):
                if cell.state.name != "REVEALED":
                    cell.state = cell.state.REVEALED
                    st.session_state.moves.append((r, c))
                    if getattr(cell, "is_mine", False):
                        st.session_state.mines_left -= 1
                    st.experimental_rerun()
            # Overlay label and probability as HTML
            cols[c].markdown(
                f"""
                <div style="background:{bg};border-radius:8px;padding:0.2em 0;">
                    {label}
                    <div style="font-size:0.7em;color:#888;">{prob:.0%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

def main():
    board = st.session_state.board
    assessor = st.session_state.assessor
    probs = cached_probs(board)

    st.title("AI-Minesweeper • Hybrid Risk Demo")
    draw_board(board, probs)

    if st.button("Solver move"):
        r, c = assessor.choose_move()
        cell = board.grid[r][c]
        if cell.state.name != "REVEALED":
            cell.state = cell.state.REVEALED
            st.session_state.moves.append((r, c))
            if getattr(cell, "is_mine", False):
                st.session_state.mines_left -= 1
            st.session_state.assessor = RiskAssessor(board)
            st.experimental_rerun()

    if st.session_state.mines_left == 0:
        st.balloons()
        st.success("All mines found! 🎉")

    st.sidebar.write(f"**Moves taken:** {len(st.session_state.moves)}")
    st.sidebar.write(f"**Mines left:** {st.session_state.mines_left}")

if __name__ == "__main__":
    main()

