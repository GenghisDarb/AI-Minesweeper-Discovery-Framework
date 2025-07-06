import streamlit as st


def display_confidence(conf: float, mode: str = "gui"):
    """
    Display solver confidence in GUI or CLI mode.
    :param conf: Confidence level (0.0 to 1.0).
    :param mode: Display mode ('gui' for Streamlit, 'cli' for terminal).
    """
    if mode == "gui":
        st.progress(conf)
        st.write(f"Solver Confidence: {conf * 100:.1f}%")
    elif mode == "cli":
        bar_length = 20
        green_length = int(conf * bar_length)
        red_length = bar_length - green_length
        bar = f"\x1b[42m{'█' * green_length}\x1b[41m{'█' * red_length}\x1b[0m"
        print(f"Confidence: {conf * 100:.1f}% [{bar}]")
