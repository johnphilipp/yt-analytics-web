from utils import sb
from utils import app
from components import analysis_sentiment
from components import analysis_wordcloud
from components import analysis_topflop
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
            analysis_sentiment.get_sentiment()

        elif menu == "Wordcloud":
            analysis_wordcloud.get_wordcloud()

        elif menu == "Top/Flop":
            analysis_topflop.get_topflop()
