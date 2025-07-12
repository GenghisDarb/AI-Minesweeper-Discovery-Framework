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

class BarMeter:
    """
    Displays a confidence bar in the CLI or GUI.

    Attributes:
        confidence (float): Confidence value between 0 and 1.
    """

    def __init__(self, confidence: float):
        self.confidence = confidence

    def render_cli(self):
        """
        Renders the confidence bar in the CLI.
        """
        bar_length = 20
        filled_length = int(self.confidence * bar_length)
        bar = "■" * filled_length + "□" * (bar_length - filled_length)
        print(f"CONFIDENCE {bar} {self.confidence * 100:.0f} %")

    def render_gui(self):
        """
        Placeholder for GUI rendering.
        """
        pass
