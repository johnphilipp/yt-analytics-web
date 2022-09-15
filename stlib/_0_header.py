import streamlit as st
from utils import app


def run():
    st.set_page_config(layout="centered", page_icon="🚗",
                       page_title="YouTube Comment Analyzer")

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>",
                    unsafe_allow_html=True)

    st.header("📊 Sentience")
    app.space(1)


if __name__ == "__main__":
    run()
