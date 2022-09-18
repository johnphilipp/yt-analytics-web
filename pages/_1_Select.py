import streamlit as st
from components import header
from components import form
from utils import app
from utils import sb


@st.cache(suppress_st_warning=True)
def _get_meta_data(video_ids):
    """
    Get meta data from sb
    Cached with in-built st caching, only rerun when
    `st.session_state["available_video_ids"]` changed
    """
    meta = []
    for video_id in video_ids:
        meta.append(sb.get_meta(video_id))
    return meta


def _catalogue(meta):
    """
    Display catalogue
    """
    def _catalogue_tile(meta):
        """
        Display catalogue tile for each video_id meta
        """
        col1, col2, col3, col4, col5 = st.columns([2, 2.2, 1.1, 1.1, 1.1])
        col1.image(meta["thumbnail_url"], width=180)
        col2.metric(label="Channel", value=meta["channel_title"])
        col3.metric(label="Views", value=app.human_format(
            int(meta["view_count"])))
        col4.metric(label="Comments", value=app.human_format(
            int(meta["comment_count"])))
        col5.text("")
        selected_add = col5.button("View Analysis", key=meta["video_id"])

        if selected_add:
            if "video_ids_selected" not in st.session_state:
                st.session_state["video_ids_selected"] = []
            if (meta["video_id"] not in st.session_state["video_ids_selected"]):
                st.session_state["video_ids_selected"].append(meta["video_id"])
            # TODO: Switch page

    for i in range(0, len(meta)):
        _catalogue_tile(meta[i])
        app.space(2)


def run():
    header.display()

    with st.expander("Edit selection 🚗"):
        form.display()

    if "available_video_ids" not in st.session_state:  # Used in utils/form.py
        st.session_state["available_video_ids"] = []

    if (st.session_state["available_video_ids"]):
        app.space(2)
        data = _get_meta_data(st.session_state["available_video_ids"])
        _catalogue(data)
    else:
        st.warning("Please select a Car to get started")


if __name__ == "__main__":
    run()
