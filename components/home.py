from utils import sb
from utils import app
import streamlit as st
import pandas as pd


def home():
    # Select Cars

    st.subheader("Select Car 🚗")
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

    # -----------------------------------------------------------------------

    # Edit Selection

    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("Edit Selection ⚙️")
        app.space(1)
        for video_id in st.session_state['video_ids_selected']:
            app.display_edit(video_id, sb.get_meta(video_id))
            app.space(1)

    # -----------------------------------------------------------------------

    # View Sentiment

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
        st.subheader("View Sentiment 📊")
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
