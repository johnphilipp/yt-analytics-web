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
from utils import app
from utils import content
from utils import fbase

#-----------------------------------------------------------------------

# Connect to Firebase

if not firebase_admin._apps:
	fbase.firebase_init()
db = firestore.client()

#-----------------------------------------------------------------------

# Set page header (just text)

st.set_page_config(layout="centered", page_icon="🚗", page_title="YouTube Comment Analyzer")
st.markdown("<h1 style='text-align: center; color: white;'>WDYT ?</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white; position: relative; bottom: 20px;'>🚗 🤔 💬 📊</h4>", unsafe_allow_html=True)


#-----------------------------------------------------------------------

# Get started section

st.subheader("Select")
st.markdown("<a style='text-align: left; color: gray; position: relative; bottom: 15px;'>\
            Choose a brand and model.\
            </a>", unsafe_allow_html=True)

# Create dropdown with values from firebase
brand = st.selectbox( # can this be empty on first run?
    'Select Brand',
    fbase.get_brands(db))
model = st.selectbox(
    'Select Model',
    fbase.get_models(db, brand))
app.space(2)

# Initialize 'video_ids_fetched' session state
if 'video_ids_fetched' not in st.session_state:
    st.session_state['video_ids_fetched'] = []

# Initialize 'video_ids' session state
if 'video_ids_selected' not in st.session_state:
    st.session_state['video_ids_selected'] = []

# Write new 'video_ids_fetched' session state
if brand != "" and model != "":
    st.session_state['video_ids_fetched'] = fbase.get_video_ids(db, brand, model)

# Display content of each element (video_id) in 'video_ids_fetched' session state
if len(st.session_state['video_ids_fetched']) > 0:
    for video_id in st.session_state['video_ids_fetched']:
        video_data = fbase.get_video_stats(db, brand, model, video_id)
        app.display_video_data(video_id, video_data, "_select")
        app.space(1)    

#-----------------------------------------------------------------------

st.subheader("Modify")
st.markdown("<a style='text-align: left; color: gray; position: relative; bottom: 15px;'>\
            Keep up to 3 videos.\
            </a>", unsafe_allow_html=True)

# st.text(st.session_state['video_ids_selected'])
if len(st.session_state['video_ids_selected']) > 0:
    for video_id in st.session_state['video_ids_selected']:
        video_data = fbase.get_video_stats(db, brand, model, video_id)
        app.display_video_data(video_id, video_data, "_modify")
        app.space(1)    
    



#-----------------------------------------------------------------------

st.subheader("Analyze")
st.markdown("<a style='text-align: left; color: gray; position: relative; bottom: 15px;'>\
            View the results.\
            </a>", unsafe_allow_html=True)