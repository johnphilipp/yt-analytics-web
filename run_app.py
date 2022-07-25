from utils import sb
from utils import app
import streamlit as st
import pandas as pd


# -----------------------------------------------------------------------

# Set page header (just text)

st.set_page_config(layout="centered", page_icon="🚗",
                   page_title="YouTube Comment Analyzer")

# -----------------------------------------------------------------------

# Get started section

# Create dropdown with values from firebase
make = st.sidebar.selectbox(  # can this be empty on first run?
    'Select Make',
    sb.get_makes())
model = st.sidebar.selectbox(
    'Select Model',
    sb.get_models(make))
trim = st.sidebar.selectbox(
    'Select Model',
    sb.get_trim(make, model))
year = st.sidebar.selectbox(
    'Select Model',
    sb.get_year(make, model, trim))
app.space_sidebar()

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
    for video_id in st.session_state['video_ids_fetched']:
        meta = sb.get_meta(video_id)
        app.display_meta(video_id, meta)
        app.space_sidebar(1)

# -----------------------------------------------------------------------

if len(st.session_state['video_ids_fetched']) > 0:
    columns = ["feature", "comment_count", "sentiment_mean", "car"]
    feature_stats = pd.DataFrame(columns=columns)
    for vid in st.session_state['video_ids_selected']:
        current = sb.get_feature_stats(vid)
        current['car'] = sb.get_car_from_video_id(vid)
        # print(current.head())
        feature_stats = pd.concat([feature_stats, current])
        feature_stats = feature_stats[feature_stats.groupby('feature')["feature"].transform(len)
                                      > (len(st.session_state['video_ids_fetched']) - 1)]
        feature_stats = feature_stats.sort_values(by=['feature'])
        feature_stats.insert(0, 'car', feature_stats.pop('car'))
        print("")
        print("")
        print("")
        print(feature_stats)
        print("")
        print("")
        print("")
        # print(st.session_state['video_ids_selected'])
        # print(feature_stats.head())
        print("")

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
