"""
Minimal Streamlit UI for the AI-Hypothesis Discovery solver.
Run with:  streamlit run streamlit_app.py
"""

import streamlit as st
import random
import os
import glob
import pandas as pd
import json

from ai_minesweeper.board_builder import BoardBuilder

# Set page configuration
st.set_page_config(page_title="AI Minesweeper – Discovery Framework", layout="wide")

# --- Sidebar: χ‑Phase Constants ---
def load_chi_constants():
    try:
        with open("data/chi_50digits.txt", "r") as f:
            chi = f.read().strip()
    except FileNotFoundError:
        chi = "N/A"

    try:
        with open("data/confidence_fit_params.json", "r") as f:
            tau = json.load(f).get("tau", "N/A")
    except FileNotFoundError:
        tau = "N/A"

    try:
        s_stat = pd.read_csv("reports/prime_residue_S.csv").iloc[-1, 0]
    except (FileNotFoundError, IndexError):
        s_stat = "N/A"

    return chi, tau, s_stat

chi, tau, s_stat = load_chi_constants()

with st.sidebar:
    st.header("χ‑Phase Constants")
    st.write(f"χ (chi): {chi}")
    st.write(f"τ (tau): {tau}")
    st.write(f"S‑stat: {s_stat}")

# --- Sidebar: Data Source Selection ---
with st.sidebar:
    st.header("Data Source")
    source_option = st.radio("Select Source", ["Example Board", "Load Dataset"])

    if source_option == "Example Board":
        example_files = sorted(glob.glob("examples/boards/*.csv"))
        example_names = [os.path.basename(f) for f in example_files]
        selected_example = st.selectbox("Example Boards", ["(none)"] + example_names)
    elif source_option == "Load Dataset":
        domain_options = ["Prime Number Spiral", "Phase-Lock φ Reset", "Periodic Table (Element Discovery)", "Custom Data Upload"]
        selected_domain = st.selectbox("Dataset Domains", domain_options)
        if selected_domain == "Custom Data Upload":
            uploaded_file = st.file_uploader("Upload Dataset", type=["csv"])

    if st.button("Load Board"):
        if source_option == "Example Board" and selected_example != "(none)":
            board_path = os.path.join("examples/boards", selected_example)
            board = BoardBuilder.from_csv(board_path)
        elif source_option == "Load Dataset":
            if selected_domain == "Custom Data Upload" and uploaded_file is not None:
                board = BoardBuilder.from_csv(uploaded_file)
            else:
                board = [["hidden"] * 8 for _ in range(8)]  # Placeholder for demo domains
        else:
            st.warning("Please select a valid board or upload a dataset.")
            st.stop()

        st.session_state.board = board
        st.session_state.revealed = [[False] * len(board[0]) for _ in board]
        st.session_state.moves = 0
        st.session_state.discovery_halted = False
        st.session_state.discovery_converged = False

# --- Main Interface: Tabs ---
tabs = st.tabs(["Game Board", "χ‑brot Visualizer", "Confidence Fit"])

with tabs[0]:
    st.header("Game Board")
    if "board" in st.session_state:
        board = st.session_state.board
        for r, row in enumerate(board):
            cols = st.columns(len(row))
            for c, cell in enumerate(row):
                if st.session_state.revealed[r][c]:
                    cols[c].write(cell)
                else:
                    if cols[c].button("", key=f"{r}-{c}"):
                        st.session_state.revealed[r][c] = True
                        st.session_state.moves += 1

with tabs[1]:
    st.header("χ‑brot Visualizer")
    st.image("figures/torus_brot_demo.png", caption="χ‑brot Fractal Field", use_column_width=True)

with tabs[2]:
    st.header("Confidence Fit")
    st.image("figures/confidence_fit.png", caption="Confidence Oscillation Fit", use_column_width=True)
    st.write(f"τ (tau): {tau}")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("Version 1.0 | [GitHub Repository](https://github.com/GenghisDarb/AI-Minesweeper-Discovery-Framework)")
