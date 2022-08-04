from utils import app
from utils import sb
import streamlit as st


# -----------------------------------------------------------------------

# Helper Func -- Edit tile

def _display_edit(video_id, meta):
    car_info = sb.get_car_from_video_id(video_id)
    col1, col2, col3, col4, col5 = st.columns([0.6, 3.2, 1.2, 1.2, 1.2])
    selected = col1.button('-', key=video_id + "_remove")
    # Remove selected videos from list
    if selected and video_id in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].remove(video_id)
        st.experimental_rerun()
    col2.text(car_info["make"] + " " +
              car_info["model"] + " (" +
              car_info["trim"] + ", " +
              str(car_info["year"]) + ")")
    col3.text(meta["channel_title"])
    col4.text(app.human_format(int(meta["view_count"])) + " views")
    col5.text(app.human_format(int(meta["comment_count"])) + " comments")


# -----------------------------------------------------------------------

# Main Func -- Edit selection

def edit_selection():
    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("Edit Selection ⚙️")
        app.space(1)
        for video_id in st.session_state['video_ids_selected']:
            _display_edit(video_id, sb.get_meta(video_id))
            app.space(1)
