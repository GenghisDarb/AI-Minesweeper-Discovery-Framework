"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
import random

# --- Dummy RiskAssessor for demonstration ---
class RiskAssessor:
    @staticmethod
    def choose_move(board):
        # Pick a random hidden cell
        hidden = [(r, c) for r, row in enumerate(board) for c, v in enumerate(row) if v == "hidden"]
        return random.choice(hidden) if hidden else None

# --- Board helpers ---
def new_board(rows, cols, mines):
    board = [["hidden" for _ in range(cols)] for _ in range(rows)]
    mine_positions = set(random.sample(range(rows * cols), mines))
    for idx in mine_positions:
        r, c = divmod(idx, cols)
        board[r][c] = "mine"
    return board

def reveal(board, r, c):
    if board[r][c] == "mine":
        return "mine"
    # Count adjacent mines
    rows, cols = len(board), len(board[0])
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "mine":
                count += 1
    return str(count) if count > 0 else "empty"

# --- Session state ---
BOARD_ROWS = 8
BOARD_COLS = 8
BOARD_MINES = 10

if "board" not in st.session_state:
    st.session_state.board = new_board(BOARD_ROWS, BOARD_COLS, BOARD_MINES)
    st.session_state.revealed = [[False]*BOARD_COLS for _ in range(BOARD_ROWS)]
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.win = False

def reset_board():
    st.session_state.board = new_board(BOARD_ROWS, BOARD_COLS, BOARD_MINES)
    st.session_state.revealed = [[False]*BOARD_COLS for _ in range(BOARD_ROWS)]
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.win = False

def check_win():
    # Win if all non-mine cells are revealed
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if st.session_state.board[r][c] != "mine" and not st.session_state.revealed[r][c]:
                return False
    return True

# --- Sidebar stats ---
with st.sidebar:
    st.header("Stats")
    st.write(f"Moves: {st.session_state.moves}")
    st.write(f"Mines: {sum(cell == 'mine' for row in st.session_state.board for cell in row)}")
    if st.session_state.game_over:
        st.error("💥 Game Over!")
    elif st.session_state.win:
        st.success("🎉 You Win!")

st.title("AI Minesweeper")

# --- Reset button ---
if st.button("Reset Board"):
    reset_board()
    st.rerun()

# --- Solver move button ---
if not st.session_state.game_over and not st.session_state.win:
    if st.button("Solver Move"):
        move = RiskAssessor.choose_move([
            ["hidden" if not st.session_state.revealed[r][c] else st.session_state.board[r][c]
             for c in range(BOARD_COLS)] for r in range(BOARD_ROWS)
        ])
        if move:
            r, c = move
            if st.session_state.board[r][c] == "mine":
                st.session_state.revealed[r][c] = True
                st.session_state.moves += 1
                st.session_state.game_over = True
            else:
                st.session_state.revealed[r][c] = True
                st.session_state.moves += 1
                if check_win():
                    st.session_state.win = True
            st.rerun()

# --- Grid display ---
for r in range(BOARD_ROWS):
    cols = st.columns(BOARD_COLS)
    for c in range(BOARD_COLS):
        key = f"{r}-{c}"
        if st.session_state.revealed[r][c]:
            val = st.session_state.board[r][c]
            if val == "mine":
                cols[c].button("💣", key=key, disabled=True, help="Mine", type="secondary", use_container_width=True)
            else:
                num = reveal(st.session_state.board, r, c)
                if num == "empty":
                    cols[c].button("⬜", key=key, disabled=True, use_container_width=True)
                else:
                    # Use markdown for blue digits
                    cols[c].markdown(
                        f"<span style='color:blue;font-weight:bold'>{num}</span>",
                        unsafe_allow_html=True,
                    )
        else:
            if not st.session_state.game_over and not st.session_state.win:
                if cols[c].button("⬜", key=key, use_container_width=True):
                    if st.session_state.board[r][c] == "mine":
                        st.session_state.revealed[r][c] = True
                        st.session_state.moves += 1
                        st.session_state.game_over = True
                    else:
                        st.session_state.revealed[r][c] = True
                        st.session_state.moves += 1
                        if check_win():
                            st.session_state.win = True
                    st.rerun()
            else:
                cols[c].button("⬜", key=key, disabled=True, use_container_width=True)

