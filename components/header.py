import streamlit as st


def display():
    """
    Display header
    """
    st.markdown("""# 📊 <a href="/" target="_self" style="font-family: 'Courier New', monospace; color: white; text-decoration: none;">senty</a>""",
                unsafe_allow_html=True)
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
