import streamlit as st
import pandas as pd
import sys
from PIL import Image
import requests
from io import BytesIO
import toml
import firebase_admin
from firebase_admin import credentials, firestore
sys.path.insert(1, "/Users/philippjohn/Developer/youtube-analytics/")
from utils.video import Video 
from utils import features
from utils import app2
from utils import yt
from utils import fb

#-----------------------------------------------------------------------

# Connect to Firebase

if not firebase_admin._apps:
	fb.firebase_init()
db = firestore.client()

#-----------------------------------------------------------------------

# Set page header (just text)

st.set_page_config(layout="centered", page_icon="🚗", page_title="YouTube Comment Analyzer")

#-----------------------------------------------------------------------

# Get started section

# Create dropdown with values from firebase
brand = st.sidebar.selectbox( # can this be empty on first run?
    'Select Brand',
    fb.get_brands(db))
model = st.sidebar.selectbox(
    'Select Model',
    fb.get_models(db, brand))
app2.space_sidebar()

# Initialize 'video_ids_fetched' session state
if 'video_ids_fetched' not in st.session_state:
    st.session_state['video_ids_fetched'] = []

# Initialize 'video_ids' session state
if 'video_ids_selected' not in st.session_state:
    st.session_state['video_ids_selected'] = []

# Write new 'video_ids_fetched' session state
if brand != "" and model != "":
    st.session_state['video_ids_fetched'] = fb.get_video_ids(db, brand, model)

# Display content of each element (video_id) in 'video_ids_fetched' session state
if len(st.session_state['video_ids_fetched']) > 0:
    for video_id in st.session_state['video_ids_fetched']:
        video_data = fb.get_video_stats(db, brand, model, video_id)
        app2.display_video_data(video_id, video_data)
        app2.space_sidebar(1)    

#-----------------------------------------------------------------------


# Read df 
vid = "data/#Merge/58.csv"
merged_videos = pd.read_csv(vid, header=[0], lineterminator='\n')

# Display videos that are in merged set
all_videos = merged_videos["car"].unique().tolist()
videos = st.multiselect("Select cars to visualize", all_videos, all_videos)

# Display features that are in merged set
all_features = merged_videos["feature"].unique().tolist()
feature_list_visualize = st.multiselect("Select features to visualize", all_features, all_features)
app2.space(1)

merged_videos = merged_videos[merged_videos["car"].isin(videos)]
merged_videos = merged_videos[merged_videos["feature"].isin(feature_list_visualize)]
app2.radar_chart(merged_videos)