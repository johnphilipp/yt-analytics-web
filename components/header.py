from utils import app
import streamlit as st

# -----------------------------------------------------------------------

# Header


def header():
    st.set_page_config(layout="centered", page_icon="🚗",
                       page_title="YouTube Comment Analyzer")
    st.header("📊 Senty")
    app.space(2)
