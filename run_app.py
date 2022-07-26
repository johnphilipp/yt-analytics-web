from utils import sb
from utils import app
import streamlit as st
import pandas as pd


# -----------------------------------------------------------------------

# Set page header (just text)

st.set_page_config(layout="centered", page_icon="🚗",
                   page_title="YouTube Comment Analyzer")

st.header("What People Say About Your Product")
app.space(2)

# -----------------------------------------------------------------------

# Get started section

# Create dropdown with values from firebase
st.subheader("Select Car 🚗")
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

# Initialize 'video_ids_fetched' session state
if 'video_ids_fetched' not in st.session_state:
    st.session_state['video_ids_fetched'] = []

# Initialize 'video_ids' session state
if 'video_ids_selected' not in st.session_state:
    st.session_state['video_ids_selected'] = []

# Write new 'video_ids_fetched' session state
if make != "" and model != "":
    car_id = sb.get_car_id(make, model, trim, year)
    st.session_state['video_ids_fetched'] = sb.get_video_ids_for_car(car_id)

# Display meta content of each element (video_id) in 'video_ids_fetched' session state
if len(st.session_state['video_ids_fetched']) > 0:
    st.subheader("Select Videos 🎥")
    for video_id in st.session_state['video_ids_fetched']:
        meta = sb.get_meta(video_id)
        app.display_meta(video_id, meta)
        app.space(2)
        st.markdown("---")
        app.space(2)

# -----------------------------------------------------------------------

if len(st.session_state['video_ids_fetched']) > 0:
    def get_feature_stats():
        feature_stats = pd.DataFrame(
            columns=["feature", "comment_count", "sentiment_mean", "car"])
        for vid in st.session_state['video_ids_selected']:
            current = sb.get_feature_stats(vid)
            current['car'] = sb.get_car_from_video_id(vid)
            feature_stats = pd.concat(
                [feature_stats, current]).sort_values(by=["feature", "car"])
            feature_stats.insert(0, 'car', feature_stats.pop('car'))
        return feature_stats

if len(st.session_state['video_ids_selected']) > 0:
    st.subheader("View Sentiment 📊")
    feature_stats = get_feature_stats()
    feature_stats = feature_stats[feature_stats.groupby(
        'feature')['feature'].transform('size') > (len(st.session_state['video_ids_selected']) - 1)]
    print(len(st.session_state['video_ids_fetched']))
    print(feature_stats)

    # Display videos that are in merged set
    all_videos = feature_stats["car"].unique().tolist()
    videos = st.multiselect("Select cars to visualize", all_videos, all_videos)

    # Display features that are in merged set
    all_features = feature_stats["feature"].unique().tolist()
    feature_list_visualize = st.multiselect(
        "Select features to visualize", all_features, all_features)
    app.space(1)

    app.radar_chart(feature_stats)

# # Read df
# vid = "data/#Merge/58.csv"
# merged_videos = pd.read_csv(vid, header=[0], lineterminator='\n')

# merged_videos = merged_videos[merged_videos["car"].isin(videos)]
# merged_videos = merged_videos[merged_videos["feature"].isin(
#     feature_list_visualize)]
# app2.radar_chart(merged_videos)
