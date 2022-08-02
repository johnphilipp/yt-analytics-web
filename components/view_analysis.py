from utils import sb
from utils import app
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


def view_analysis():
    def get_feature_stats():
        feature_stats = pd.DataFrame(
            columns=["feature", "comment_count", "sentiment_mean", "car"])
        for vid in st.session_state['video_ids_selected']:
            current = sb.get_feature_stats(vid)
            car_info = sb.get_car_from_video_id(vid)
            current['car'] = \
                car_info["make"] + " " + \
                car_info["model"] + " " + \
                car_info["trim"] + " " + \
                str(car_info["year"]) + " (" + \
                vid + ")"
            feature_stats = pd.concat(
                [feature_stats, current]).sort_values(by=["feature", "car"])
            feature_stats.insert(0, 'car', feature_stats.pop('car'))
        return feature_stats

    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("View Analysis 📊")
        menu = option_menu(None, ["Sentiment", "Wordcloud"],
                           icons=['bar-chart', 'type'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Sentiment":
            app.space(2)

            feature_stats = get_feature_stats()
            feature_stats = feature_stats[feature_stats.groupby(
                'feature')['feature'].transform('size') > (len(st.session_state['video_ids_selected']) - 1)]

            # Display radar chart
            app.radar_chart(feature_stats)

            # Display features that are in merged set
            all_features = feature_stats["feature"].unique().tolist()
            st.multiselect("Edit features to visualize",
                           all_features, all_features)
            app.space(1)

        elif menu == "Wordcloud":
            st.write("Wordcloud")
            df = pd.DataFrame(sb.get_content(
                st.session_state['video_ids_selected'][0]), columns=['content'])
            app.wordcloud(df)
