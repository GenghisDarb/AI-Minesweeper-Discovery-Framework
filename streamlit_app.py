"""
Minimal Streamlit UI for the AI-Minesweeper solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
import random
import os
import glob
import pandas as pd
import json
import sys

sys.path.append("src")  # Add src directory to Python path

from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.solver import ConstraintSolver
from torus_brot.renderers.torus_brot_renderer import render_grid


# --- Dummy RiskAssessor for demonstration ---
class RiskAssessor:
    @staticmethod
    def choose_move(board):
        # Pick a random hidden cell
        hidden = [
            (r, c)
            for r, row in enumerate(board)
            for c, v in enumerate(row)
            if v == "hidden"
        ]
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
    st.session_state.revealed = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.win = False


def reset_board():
    st.session_state.board = new_board(BOARD_ROWS, BOARD_COLS, BOARD_MINES)
    st.session_state.revealed = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]
    st.session_state.moves = 0
    st.session_state.game_over = False
    st.session_state.win = False


def check_win():
    # Win if all non-mine cells are revealed
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if (
                st.session_state.board[r][c] != "mine"
                and not st.session_state.revealed[r][c]
            ):
                return False
    return True


def _init_state(board):
    st.session_state.board = board
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    st.session_state.revealed = [[False] * cols for _ in range(rows)]
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
    st.write(
        f"Mines: {sum(cell == 'mine' for row in st.session_state.board for cell in row)}"
    )
    if st.session_state.game_over:
        st.error("💥 Game Over!")
    elif st.session_state.win:
        st.success("🎉 You Win!")

st.title("AI Minesweeper – Hypothesis Discovery Framework")
st.sidebar.title("Settings")

# --- Startup Menus ---
# LLM Selection
llm_options = ["None (Logic-only)", "OpenAI GPT-4", "Anthropic Claude", "Local Model"]
selected_llm = st.sidebar.selectbox(
    "Choose an AI assistant (LLM) for parsing/heuristics:", llm_options, index=0
)
st.session_state.selected_llm = selected_llm

# Domain Selection
domains = [
    "Prime Number Spiral",
    "Phase-Lock φ Reset",
    "Periodic Table (Element Discovery)",
    "Custom Data Upload",
]
selected_domain = st.sidebar.selectbox("Choose a dataset/domain to explore:", domains)
st.session_state.selected_domain = selected_domain

# Ensure selections are made before proceeding
if not selected_domain or not selected_llm:
    st.warning("Please select an LLM and a domain to proceed.")
    st.stop()

# --- Board Initialization ---
if selected_domain == "Custom Data Upload":
    # Update file uploader logic to support text and PDF
    uploaded_file = st.sidebar.file_uploader(
        "Upload data (CSV, TXT, PDF, TEX)", type=["csv", "txt", "pdf", "tex"]
    )
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        data = uploaded_file.read()
        if file_type == "csv":
            board = BoardBuilder.from_csv(data)
        elif file_type in ["txt", "tex"]:
            text = data.decode("utf-8", errors="ignore")
            board = BoardBuilder.from_text(text)
        elif file_type == "pdf":
            board = BoardBuilder.from_pdf(data)
        else:
            st.error("Unsupported file type")
            st.stop()
        st.session_state.board = board
        st.experimental_rerun()
else:
    # Load preset boards for demo domains
    demo_boards = {
        "Prime Number Spiral": new_board(8, 8, 10),
        "Phase-Lock φ Reset": new_board(8, 8, 10),
        "Periodic Table (Element Discovery)": new_board(8, 8, 10),
    }
    st.session_state.board = demo_boards.get(selected_domain, new_board(8, 8, 10))

# Load example board
example_path = "examples/boards/mini.csv"
board = BoardBuilder.from_csv(example_path)
st.session_state.board = board

# Debugging output
print(f"Board type: {type(board)}")

# Debugging output after BoardBuilder.from_csv
print(f"Board type after from_csv: {type(board)}")

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
                col.markdown(
                    f"<span style='color:blue;'>{cell.adjacent_mines}</span>",
                    unsafe_allow_html=True,
                )
        elif cell.state == State.FLAGGED:
            col.markdown("🚩")

# Solver interaction
if st.button("Solver Move"):
    ConstraintSolver.solve(board, max_moves=1)

# Add LLM selection menu
llm_choice = st.selectbox(
    "Select LLM:", ["None", "OpenAI", "Anthropic Claude", "Local (ollama)"]
)

# Add dataset menu based on LLM choice
if llm_choice:
    dataset_choice = st.selectbox(
        "Select Dataset:",
        [
            "TORUS demo",
            "Cymatics demo",
            "Prime-spiral demo",
            "Periodic-table (isotope)",
            "Upload file…",
        ],
    )

    # Guard against re-runs
    if "initialised" not in st.session_state:
        st.session_state.initialised = False

    if not st.session_state.initialised:
        # Load domain and render grid
        board, meta = DomainLoader.load(
            dataset_choice, None
        )  # Replace None with uploaded file logic
        st.session_state.initialised = True
        st.write("Board loaded:", board)


class DomainLoader:
    @staticmethod
    def load(domain_name, uploaded_file):
        if domain_name == "TORUS demo":
            # Example logic for loading TORUS demo
            return [["hidden"] * 10 for _ in range(10)], {"meta": "TORUS demo metadata"}
        elif domain_name == "Cymatics demo":
            # Example logic for loading Cymatics demo
            return [["hidden"] * 8 for _ in range(8)], {"meta": "Cymatics demo metadata"}
        elif domain_name == "Prime-spiral demo":
            # Example logic for loading Prime-spiral demo
            return [["hidden"] * 12 for _ in range(12)], {"meta": "Prime-spiral demo metadata"}
        elif domain_name == "Periodic-table (isotope)":
            # Example logic for loading Periodic-table demo
            return [["hidden"] * 7 for _ in range(7)], {"meta": "Periodic-table metadata"}
        else:
            raise ValueError(f"Unknown domain: {domain_name}")


# Add dataset menu entry for Periodic-table (isotope)
dataset_choice = st.selectbox(
    "Select Dataset:",
    [
        "TORUS demo",
        "Cymatics demo",
        "Prime-spiral demo",
        "Periodic-table (isotope)",
        "Upload file…",
    ],
)

if dataset_choice == "Periodic-table (isotope)":
    board = DomainLoader.load("periodic-table-v2")
    st.session_state.board = board

# Display tooltips for cells
for r, row in enumerate(st.session_state.board.grid):
    for c, cell in enumerate(row):
        tooltip = (
            "🟦 Weighted mine count"
            if cell.adjacent_mine_weight > 0
            else "❔ Unexplored isotope"
        )
        if cell.is_mine:
            tooltip = "🚩 Predicted unbound isotope"
        st.write(f"Cell ({r}, {c}): {tooltip}")

# Sidebar stats
flagged_cells = sum(
    1
    for cell in st.session_state.board.cells
    if cell.is_mine and cell.state == "FLAGGED"
)
st.sidebar.write(
    f"Predicted-stable blanks flagged: {flagged_cells} / {len(st.session_state.board.cells)}"
)

# Handle the TORUS-brot domain selection
if selected_domain == "TORUS-brot Fractal":
    # Load default parameters for the fractal
    fractal_params_path = "torus_brot/data/sample_params.json"
    renderer = TorusBrotRenderer(fractal_params_path)

    # Render the fractal image
    fractal_image_path = renderer.render_to_image("torus_brot_output.png")

    # Display the fractal image in the UI
    st.image(fractal_image_path, caption="TORUS-brot Fractal", use_column_width=True)

# Add Meta-Cell Confidence Module toggle
use_meta = st.sidebar.checkbox("Enable Meta-Cell (Adaptive Confidence)", value=True)

# Initialize solver based on toggle
if use_meta:
    from ai_minesweeper.meta_cell_confidence.policy_wrapper import ConfidencePolicy
    from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence

    solver = ConfidencePolicy(RiskAssessor, BetaConfidence())
else:
    solver = RiskAssessor()

# Display solver confidence in sidebar
if use_meta:
    st.sidebar.write(f"Solver confidence: {solver.confidence.mean():.2f}")
    st.sidebar.progress(solver.confidence.mean())

# Update solver logic for moves
if st.button("Solver Move"):
    move = solver.choose_move(st.session_state.board)
    if move:
        r, c = move
        outcome = reveal(st.session_state.board, r, c) != "mine"
        solver.confidence.update(prediction=solver.last_prob, outcome=outcome)
        st.session_state.moves += 1
        st.experimental_rerun()

# Sidebar constants section
st.sidebar.markdown("### χ‑Phase Constants")

# Load χ
with open("data/chi_50digits.txt") as f:
    chi = f.read().strip()

# Load fit params
with open("data/confidence_fit_params.json") as f:
    params = json.load(f)

# Load S
with open("reports/prime_residue_S.csv") as f:
    s_row = f.read().strip().split(",")
    S = float(s_row[-1])

st.sidebar.text(f"χ = {chi}")
st.sidebar.text(f"τ ≈ {params['τ']:.2f}")
st.sidebar.text(f"S‑stat = {S:.6f}")

# Visual tabs
tab1, tab2, tab3 = st.tabs(["Game Board", "χ‑brot Visualizer", "Confidence Fit"])

with tab1:
    # existing game UI goes here
    pass

with tab2:
    st.image("figures/torus_brot_demo.png", caption="χ‑brot Escape Field", use_column_width=True)

with tab3:
    st.image("figures/confidence_fit.png", caption="Confidence Oscillation Fit", use_column_width=True)
    st.json(params)

# Load constants
with open("data/chi_50digits.txt") as f:
    chi = f.read().strip()

with open("data/confidence_fit_params.json") as f:
    fit_params = json.load(f)
    tau = fit_params["τ"]

s_statistic = pd.read_csv("reports/prime_residue_S.csv", header=None).iloc[0, -1]

# Sidebar display
st.sidebar.title("Constants")
st.sidebar.write(f"χ (Golden Log): {chi}")
st.sidebar.write(f"τ (Oscillation Period): {tau}")
st.sidebar.write(f"S-statistic: {s_statistic}")

# Tabs for visuals
tab1, tab2 = st.tabs(["χ-brot Visualizer", "Oscillation Curve Fit"])

# χ-brot Visualizer
with tab1:
    st.header("χ-brot Visualizer")
    # Generate χ-brot fractal visualization
    img = render_grid(n=400)
    st.image(img, caption="χ-brot Fractal Field", use_column_width=True)

# Oscillation Curve Fit
with tab2:
    st.header("Oscillation Curve Fit")
    st.image("figures/confidence_fit.png", caption="Damped χ Oscillation Curve")
    st.write(f"τ (Oscillation Period): {tau}")

# Board loader logic cleanup
source = st.radio("Board source", ["Example", "Dataset"])

if source == "Example":
    board_name = st.selectbox("Select example board:", ["corner trap", "triple mine", "box pattern"])
elif source == "Dataset":
    uploaded = st.file_uploader("Upload dataset JSON")

load_trigger = st.button("Load board")

if load_trigger:
    if source == "Example":
        board = load_example(board_name)  # Replace with existing logic
    elif uploaded:
        board = parse_uploaded(uploaded)  # Replace with existing logic
    else:
        st.warning("Please select a board or upload data.")

    st.session_state["board"] = board
    st.success("Board loaded.")

# Sidebar configuration
st.sidebar.title("Configuration")
use_wolfram = st.sidebar.checkbox("Use Wolfram Engine", value=False)

if use_wolfram:
    st.sidebar.write("Wolfram Engine mode enabled.")
else:
    st.sidebar.write("Using pre-generated files.")
