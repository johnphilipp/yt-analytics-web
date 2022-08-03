from utils import sb
from utils import app
from components import request
import streamlit as st

# -----------------------------------------------------------------------

# Select Cars


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
    if make != "" and model != "" and trim != "" and year != "":
        car_id = sb.get_car_id(make, model, trim, year)
        for video_id in sb.get_video_ids_for_car(car_id):
            app.display_select(video_id, sb.get_meta(video_id))
            app.space(2)
