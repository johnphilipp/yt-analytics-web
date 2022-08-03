from utils import app
from utils import sb
import streamlit as st

# -----------------------------------------------------------------------

# Edit Selection


def edit_selection():
    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("Edit Selection ⚙️")
        app.space(1)
        for video_id in st.session_state['video_ids_selected']:
            app.display_edit(video_id, sb.get_meta(video_id))
            app.space(1)
