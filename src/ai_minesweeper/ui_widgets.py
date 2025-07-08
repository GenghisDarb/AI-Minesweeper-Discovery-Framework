import streamlit as st


def display_confidence(conf: float, mode="cli") -> str:
    if mode == "cli":
        result = f"Confidence: {conf * 100:.1f}% [{'█' * int(conf * 20)}{' ' * (20 - int(conf * 20))}]"
        print(result)
        return result
    elif mode == "streamlit":
        bar = f"Confidence: {conf * 100:.1f}% [████████████████████]"
        st.markdown(bar)
        return bar
