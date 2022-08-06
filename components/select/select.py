from utils import sb
from utils import app
from components.request import request
import streamlit as st


# -----------------------------------------------------------------------

# Helper Func -- Select tile

def _display_select(video_id, meta):
    col1, col2, col3, col4, col5 = st.columns([0.5, 2, 2.2, 1.1, 1.1])
    col1.header("")
    selected = col1.button('+', key=video_id + "_add")
    # Add selected videos to list
    if selected and video_id not in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].append(video_id)
    col2.image(meta["thumbnail_url"], width=180)
    col3.metric(label="Channel", value=meta["channel_title"])
    col4.metric(label="Views", value=app.human_format(int(meta["view_count"])))
    col5.metric(label="Comments", value=app.human_format(
        int(meta["comment_count"])))


# -----------------------------------------------------------------------

# Main Func -- Select cars

def select_cars():
    col1, col2 = st.columns([3.5, 1])
    col1.subheader("Select Car 🚗")
    request_addition = col2.button("Request addition")
    if request_addition:
        request.request()
    app.space(1)
    make = st.selectbox(  # can this be empty on first run?
        'Select Make',
        sb.get_makes())
    model = st.selectbox(
        'Select Model',
        sb.get_models(make))
    trim = st.selectbox(
        'Select Trim',
        sb.get_trim(make, model))
    year = st.selectbox(
        'Select Year',
        sb.get_year(make, model, trim))
    app.space(2)
    st.markdown("---")
    app.space(2)

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
        for video_id in sb.get_video_ids_for_car(car_id):
            _display_select(video_id, sb.get_meta(video_id))
            app.space(2)
