import streamlit as st
from utils import app
from components import form
from components import header


# -----------------------------------------------------------------------

# Display landing page

def _landing_page():
    col1, col2 = st.columns([1, 2.5])

    col1.write("##")
    col1.write("##")
    col1.write("## Automotive market intelligence via social media analytics 💬")
    col1.write("##")

    col2.image("https://p-john.com/wp-content/uploads/2022/09/wallpaper.png")


# -----------------------------------------------------------------------

# Display form

def _form():
    st.write("## Select a car to get started 🚗")
    form.display()


# -----------------------------------------------------------------------

# Display value prop

def _value_prop():
    col1, col2, col3 = st.columns([1, 1, 1])

    col1.markdown("""<p style="text-align: center; font-size: 50px;">💡</p>""",
                  unsafe_allow_html=True)
    col1.markdown(
        """<h3 style="text-align: center;">
        Discover product insights via social media
        </h3>""", unsafe_allow_html=True)
    col1.write("#")

    col2.markdown("""<p style="text-align: center; font-size: 50px;">📶</p>""",
                  unsafe_allow_html=True)
    col2.markdown(
        """<h3 style="text-align: center;">
        Separate the signal from the noise
        </h3>""", unsafe_allow_html=True)
    col2.write("#")

    col3.markdown("""<p style="text-align: center; font-size: 50px;">🎯</p>""",
                  unsafe_allow_html=True)
    col3.markdown(
        """<h3 style="text-align: center;">
        Benchmark against your competition
        </h3>""", unsafe_allow_html=True)


# -----------------------------------------------------------------------

# Run

def run():
    st.set_page_config(layout="centered", page_icon="📊",
                       page_title="senty")

    header.display()

    _landing_page()
    app.space(4)

    _form()
    app.space(7)

    _value_prop()

    # st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    run()
