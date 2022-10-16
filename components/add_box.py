from components import form
import streamlit as st
from database import db
from utils import app


def display_add_box(label):
    """
    Display add box

    TODO: Display this when no car is in session state
    """
    def _update_session_state(car_id, make, model, previews):
        if model == previews["model"]:
            model = db.get_model_from_car_id(car_id)

        if make not in st.session_state["car_ids"]:
            st.session_state["car_ids"][make] = {}
        if model not in st.session_state["car_ids"][make]:
            st.session_state["car_ids"][make][model] = {}
        if car_id not in st.session_state["car_ids"][make][model]:
            st.session_state["car_ids"][make][model][car_id] = db.get_num_comments_for_car_id(
                car_id)
            return True
        else:
            return False
        # todo also add video ids on  car id, and then all comments per nvideo id.... b etter overview

    previews = form._get_previews()

    if "car_selected" not in st.session_state:
        st.session_state["car_selected"] = {
            "make": previews["make"],
            "model": previews["model"],
            "trim": previews["trim"],
            "year": previews["year"]
        }

    with st.expander(label, expanded=True):
        col1, col2 = st.columns([1, 1])

        makes = db.get_makes()
        makes.insert(0, previews["make"])
        make = col1.selectbox("Make", makes, key="make_selected")

        models = db.get_models(make)
        models.insert(0, previews["model"])
        model = col2.selectbox("Model", models)

        num_comments = app.human_format(
            db.get_num_comments_for_make_and_model(make, model))
        if num_comments == "0":
            num_comments = ""
        button = st.button("Analyze {} comments".format(num_comments))

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
                st.experimental_rerun()
