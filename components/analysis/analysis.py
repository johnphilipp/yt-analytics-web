from utils import app
from components.analysis import sentiment
from components.analysis import wordcloud
from components.analysis import topflop
import streamlit as st
from streamlit_option_menu import option_menu


# -----------------------------------------------------------------------

# Main func -- View Analysis

def view_analysis():
    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("View Analysis 📊")
        app.space(2)

        menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                           icons=['bar-chart', 'type', 'star-half'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Sentiment":
            sentiment.get_sentiment()

        elif menu == "Wordcloud":
            wordcloud.get_wordcloud()

        elif menu == "Top/Flop":
            topflop.get_topflop()
