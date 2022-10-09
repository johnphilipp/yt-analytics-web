import streamlit as st
from utils import app
from utils import sb
from utils.switch_page import switch_page
from components import header
from components import form


def _landing_page():
    """
    Display landing page
    """
    st.markdown("<h1> Get product insights <br>with <u>social analytics</u></h1>",
                unsafe_allow_html=True)

    app.space(2)

    col1, col2 = st.columns([1, 2])

    col1.markdown("<h3> Analyze my car 🚗</h3>",
                  unsafe_allow_html=True)
    col1.markdown("###")

    # ------------------------------------------------
    # Form

    previews = form._get_previews()

    if "car_selected" not in st.session_state:
        st.session_state["car_selected"] = {
            "make": previews["make"],
            "model": previews["model"],
            "trim": previews["trim"],
            "year": previews["year"]
        }

    makes = sb.get_makes()
    makes.insert(0, previews["make"])
    make = col1.selectbox("Make", makes, key="make_selected")

    col1.markdown("###")

    models = sb.get_models(make)
    models.insert(0, previews["model"])
    model = col1.selectbox("Model", models)

    app.space(1)

    button = col1.button("Analyze {} comments".format(
        form.get_button_num_comments(make, model, previews)))

    if button:
        if (make == "" or make == previews["make"]):
            st.warning("Please select a Make")
        else:
            if "car_ids_selected" not in st.session_state:
                st.session_state["car_ids_selected"] = []

            selected_cars = form.get_car_ids(make, model, previews)
            if isinstance(selected_cars, int):
                car = selected_cars
                if car not in st.session_state["car_ids_selected"]:
                    st.session_state["car_ids_selected"].append(car)
                    switch_page("analytics")
            else:
                for car in selected_cars:
                    if car not in st.session_state["car_ids_selected"]:
                        st.session_state["car_ids_selected"].append(car)
                        switch_page("analytics")

    # ------------------------------------------------

    col2.markdown("""
                  <div style='width:100%; display:block; overflow:hidden'>
                  <img style='width:100%' src='https://p-john.com/wp-content/uploads/2022/09/wallpaper.png'>
                  </div>
                  """, unsafe_allow_html=True)

    # col2.image("https://p-john.com/wp-content/uploads/2022/09/wallpaper.png")
    col2.markdown("")


def _value_prop():
    """
    Display value prop
    """
    app.space(10)

    col1, col2, col3 = st.columns([1, 1, 1])

    col1.markdown("""<p style="text-align: center; font-size: 50px;">🤖</p>""",
                  unsafe_allow_html=True)
    col1.markdown(
        """<h4 style="text-align: center;">
        Scrape and filter through millions of comments from social media
        </h4>""", unsafe_allow_html=True)
    col1.write("#")

    col2.markdown("""<p style="text-align: center; font-size: 50px;">💡</p>""",
                  unsafe_allow_html=True)
    col2.markdown(
        """<h4 style="text-align: center;">
        Gain new insights to develop your ideas and hypotheses
        </h4>""", unsafe_allow_html=True)
    col2.write("#")

    col3.markdown("""<p style="text-align: center; font-size: 50px;">🎯</p>""",
                  unsafe_allow_html=True)
    col3.markdown(
        """<h4 style="text-align: center;">
        Benchmark your products against your competition
        </h4>""", unsafe_allow_html=True)


def run():
    header.display()

    with open("style/home.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    _landing_page()

    _value_prop()

    # st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    run()
