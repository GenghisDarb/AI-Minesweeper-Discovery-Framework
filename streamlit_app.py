"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
import random
import os
import glob
import pandas as pd
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import ConstraintSolver

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

# --- BoardBuilder stub for demonstration ---
class BoardBuilder:
    @staticmethod
    def from_csv(path_or_bytes):
        if isinstance(path_or_bytes, bytes):
            df = pd.read_csv(pd.io.common.BytesIO(path_or_bytes))
        else:
            df = pd.read_csv(path_or_bytes)
        # Convert DataFrame to your board format; here we just return the DataFrame as a list of lists
        return df.values.tolist()

    @staticmethod
    def from_dataframe(df):
        return df.values.tolist()

def _init_state(board):
    st.session_state.board = board
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    st.session_state.revealed = [[False]*cols for _ in range(rows)]
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.win = False

def load_board(source):
    if isinstance(source, bytes):
        return BoardBuilder.from_csv(source)
    elif isinstance(source, str):
        return BoardBuilder.from_csv(source)
    elif isinstance(source, pd.DataFrame):
        return BoardBuilder.from_dataframe(source)
    else:
        raise ValueError("Unsupported board source type")

# --- Sidebar data source loader ---
with st.sidebar:
    st.header("🗂 Data source")
    # Example boards from examples/boards/*.csv
    example_files = sorted(glob.glob("examples/boards/*.csv"))
    example_names = [os.path.basename(f) for f in example_files]
    selected_example = st.selectbox("Example boards", ["(none)"] + example_names)
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    # Load from uploaded file
    if uploaded_file is not None:
        board = load_board(uploaded_file.read())
        _init_state(board)
        st.rerun()
    # Load from example
    elif selected_example != "(none)":
        board_path = os.path.join("examples/boards", selected_example)
        board = load_board(board_path)
        _init_state(board)
        st.rerun()

# --- Sidebar stats ---
with st.sidebar:
    st.header("Stats")
    st.write(f"Moves: {st.session_state.moves}")
    st.write(f"Mines: {sum(cell == 'mine' for row in st.session_state.board for cell in row)}")
    if st.session_state.game_over:
        st.error("💥 Game Over!")
    elif st.session_state.win:
        st.success("🎉 You Win!")

st.title("AI Minesweeper – Hypothesis Discovery Framework")
st.sidebar.title("Settings")

# Load example board
example_path = "examples/boards/mini.csv"
board = BoardBuilder.from_csv(example_path)
st.session_state.board = board

# Display board
for r in range(board.n_rows):
    cols = st.columns(board.n_cols)
    for c, col in enumerate(cols):
        cell = board.grid[r][c]
        if cell.state == State.HIDDEN:
            col.button("", key=f"{r}-{c}")
        elif cell.state == State.REVEALED:
            if cell.is_mine:
                col.markdown("💣")
            else:
                col.markdown(f"<span style='color:blue;'>{cell.adjacent_mines}</span>", unsafe_allow_html=True)
        elif cell.state == State.FLAGGED:
            col.markdown("🚩")

# Solver interaction
if st.button("Solver Move"):
    ConstraintSolver.solve(board, max_moves=1)

