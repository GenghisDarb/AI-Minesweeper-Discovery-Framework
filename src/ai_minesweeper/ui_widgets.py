import streamlit as st


def display_confidence(conf: float, mode="cli") -> str:
    if mode == "cli":
        result = f"Confidence: {conf * 100:.1f}% [{'█' * int(conf * 20)}{' ' * (20 - int(conf * 20))}]"
        print(result)
        return result
    elif mode == "streamlit":
        st.markdown(f"### Confidence Level")
        st.progress(conf)
        st.write(f"Confidence: {conf * 100:.1f}%")
        return f"Confidence: {conf * 100:.1f}%"
