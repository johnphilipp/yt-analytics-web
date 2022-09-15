from utils import app
import streamlit as st


# -----------------------------------------------------------------------

# Header

def header():
    st.set_page_config(layout="centered", page_icon="🚗",
                       page_title="YouTube Comment Analyzer")
    st.markdown(
        f"""
        <style>
            .appview-container .main .block-container{{
                max-width: 1000px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("📊 Senty")
    app.space(1)

    col1, col2 = st.columns([1, 3])

    col1.subheader("Automotive Market Intelligence")
    col1.markdown("")
    col1.markdown("✅ Learn what **Social Media** thinks about your fleet")
    col1.markdown("✅ Extract **Sentiment Analysis** of Product Features")
    col1.markdown("✅ Benchmark against your **Competiton**")
    col1.markdown("")

    col2.image(
        "https://p-john.com/wp-content/uploads/2022/09/wallpaper.png")

    app.space(2)
