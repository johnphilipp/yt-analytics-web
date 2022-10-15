import streamlit as st
from utils import app
from database import db
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

    makes = db.get_makes()
    makes.insert(0, previews["make"])
    make = col1.selectbox("Make", makes, key="make_selected")

    col1.markdown("###")

    models = db.get_models(make)
    models.insert(0, previews["model"])
    model = col1.selectbox("Model", models)

    app.space(1)

    num_comments = app.human_format(
        db.get_num_comments_for_make_and_model(make, model))
    if num_comments == "0":
        num_comments = ""
    button = col1.button("Analyze {} comments".format(num_comments))

    if button:
        def button(make, model):
            if (make == "" or make == previews["make"]):
                st.warning("Please select a Make")
            else:
                if model == previews["model"]:
                    # potentially multiple models

                    models = db.get_models_of_make(make)
                    if make not in st.session_state["cars"]:
                        st.session_state["cars"][make] = {}
                    for model in models:
                        if model not in st.session_state["cars"][make]:
                            st.session_state["cars"][make][model] = {}

                        car_ids = db.get_car_id_from_make_model(
                            make, model)
                        changes = False
                        changes = True  # figure  out where this should go
                        for car_id in car_ids:
                            if car_id not in st.session_state["cars"][make][model]:
                                changes = True
                                st.session_state["cars"][make][model][car_id] = {
                                }

                                video_ids = db.get_video_ids_for_car_id(
                                    car_id)
                                for video_id in video_ids:
                                    if video_id not in st.session_state["cars"][make][model][car_id]:
                                        st.session_state["cars"][make][model][car_id][video_id] = db.get_comment_count_actual_for_video_id(
                                            video_id)
                else:
                    if make not in st.session_state["cars"]:
                        st.session_state["cars"][make] = {}
                    if model not in st.session_state["cars"][make]:
                        st.session_state["cars"][make][model] = {}

                    car_ids = db.get_car_id_from_make_model(make, model)
                    changes = False
                    changes = True  # figure  out where this should go
                    for car_id in car_ids:
                        if car_id not in st.session_state["cars"][make][model]:
                            changes = True
                            st.session_state["cars"][make][model][car_id] = {
                            }

                            video_ids = db.get_video_ids_for_car_id(car_id)
                            for video_id in video_ids:
                                if video_id not in st.session_state["cars"][make][model][car_id]:
                                    st.session_state["cars"][make][model][car_id][video_id] = db.get_comment_count_actual_for_video_id(
                                        video_id)
                print("CARS: ", st.session_state["cars"])
                return changes

        changes = button(make, model)

        if changes:
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

    if "cars" not in st.session_state:
        st.session_state["cars"] = {}

    _landing_page()

    _value_prop()

    # st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    run()
