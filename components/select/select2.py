from utils import sb
from utils import app
from components.request import request
import streamlit as st


# -----------------------------------------------------------------------

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
