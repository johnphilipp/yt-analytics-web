import streamlit as st
from components import header
from utils import app
from utils import sb
from components.analytics import sentiment
from components.analytics import wcloud
from components.analytics import topflop
import streamlit as st
from streamlit_option_menu import option_menu


# -----------------------------------------------------------------------

# Edit tile

def _edit(video_id, meta):
    car_info = sb.get_car_from_video_id(video_id)
    col1, col2, col3, col4, col5 = st.columns([0.6, 3.2, 1.2, 1.2, 1.2])
    selected_remove = col1.button('-', key=video_id + "_remove")
    # Remove selected videos from list
    if selected_remove and video_id in st.session_state['video_ids_selected']:
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

# View Analysis

def view_analysis():
    if len(st.session_state['video_ids_selected']) > 0:
        with st.expander("Edit selection 🚗"):
            app.space(1)
            # TODO: Cache using st.session_state['video_ids_selected']
            for video_id in st.session_state['video_ids_selected']:
                _edit(video_id, sb.get_meta(video_id))
        app.space(1)

        menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                           icons=['bar-chart-fill', 'type', 'star-half'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Sentiment":
            occurrence_cutoff = st.slider(
                "Select minimum munber of feature occurrences", 1, 30, key="occurrence_cutoff")
            sentiment.get_sentiment_radar(
                st.session_state['video_ids_selected'], occurrence_cutoff)

        elif menu == "Wordcloud":
            # TODO: Cache using st.session_state['video_ids_selected']
            wcloud.get_wordcloud()

        elif menu == "Top/Flop":
            # TODO: Cache using st.session_state['video_ids_selected']
            topflop.get_topflop()


def run():
    header.display()
    if "video_ids_selected" not in st.session_state:
        st.session_state["video_ids_selected"] = []
    if st.session_state["video_ids_selected"]:
        view_analysis()
    else:
        st.warning("Please select a Car and Video to get started")


if __name__ == "__main__":
    run()
