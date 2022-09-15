from utils import sb
from utils import app
from components.request import request
import streamlit as st


# -----------------------------------------------------------------------

# Helper Func -- Select tile

def _display_select(video_id, meta):
    col1, col2, col3, col4, col5 = st.columns([2, 2.2, 1.1, 1.1, 1.1])
    col1.image(meta["thumbnail_url"], width=180)
    col2.metric(label="Channel", value=meta["channel_title"])
    col3.metric(label="Views", value=app.human_format(int(meta["view_count"])))
    col4.metric(label="Comments", value=app.human_format(
        int(meta["comment_count"])))
    col5.text("")
    selected_add = col5.button('Add to Analysis', key=video_id + "_add")
    if selected_add and video_id not in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].append(video_id)


# -----------------------------------------------------------------------

# Main Func -- Select cars

def select_cars():
    if "video_count" not in st.session_state:
        st.session_state["video_count"] = ""

    app.space(1)

    with st.form("Test"):
        st.subheader("Select a car to get started 🚗")

        col1, col2 = st.columns(2)
        make = col1.selectbox(  # can this be empty on first run?
            "Select Make",
            sb.get_makes())
        model = col2.selectbox(
            "Select Model",
            sb.get_models(make))

        col1, col2 = st.columns(2)
        trim = col1.selectbox(
            "Select Trim",
            sb.get_trim(make, model))
        year = col2.selectbox(
            "Select Year",
            sb.get_year(make, model, trim))

        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>",
                            unsafe_allow_html=True)
        local_css("style.css")
        button = st.form_submit_button("See all {} videos".format(
            st.session_state["video_count"]))

        app.space(1)

    # Initialize 'video_ids' session state
    if 'video_ids_selected' not in st.session_state:
        st.session_state['video_ids_selected'] = []

    # Display meta content of each element (video_id) in 'video_ids_fetched' session state
    st.subheader("Select Videos 🎥")
    app.space(1)

    #
    # TODO: Add "Select all videos" button
    # TODO: Add built-in video vierwer
    # TODO: Animate comment numbers"
    #

    if make != "" and model != "" and trim != "" and year != "":
        car_id = sb.get_car_id(make, model, trim, year)
        video_ids_for_car = sb.get_video_ids_for_car_id(car_id)
        st.session_state['video_ids_selected'] = str(len(video_ids_for_car))
        for video_id in video_ids_for_car:
            _display_select(video_id, sb.get_meta(video_id))
            app.space(2)
