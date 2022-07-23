from utils.video import Video 
from utils import features
from utils import app
import streamlit as st
import pandas as pd

#-----------------------------------------------------------------------

st.set_page_config(layout="centered", page_icon="🚗", page_title="YouTube Comment Analyzer")

st.markdown("<h1 style='text-align: center; color: white;'>WDYT?</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white; position: relative; bottom: 20px;'>🚗 🤔 💬 📊</h3>", unsafe_allow_html=True)
app.space(1)

st.subheader("Get Started")
st.caption("### Choose one or two YouTube videos and title the car(s) and channel(s).")
app.space(2)

col1, col2 = st.columns([1,1])
with col1:
    car1 = st.text_input('Car')
    channel1 = st.text_input('Channel')
    url1 = st.text_input('YouTube URL')
with col2:
    car2 = st.text_input('Car ')
    channel2 = st.text_input('Channel ')
    url2 = st.text_input('YouTube URL ')
app.space(1)

feature_list = st.multiselect("Features", features.get_defined_feature_list(), features.get_defined_feature_list()) # Add text_input for additional features
app.space(1)

run = st.button('Run')
app.space(1)

videos_to_merge = []

if ((run == True)):
    # Run analysis for video1
    if ((car1 != "") and (channel1 != "") and (url1 != "")):
        video1 = Video(car1, channel1, url1, feature_list)
        if (not video1.content_exists()):
            st.text("Running analysis for " + video1.get_car_name() + " / " + video1.get_channel_name())
            st.text("1) Downloading content...")
            video1.get_content()
            st.text("2) Calculating sentiment...")
            video1.get_sentiment()
            st.text("3) Generating wordcloud...")
            video1.get_wordcloud()
            st.text("4) Calculating feature stats...")
            video1.get_feature_stats()
            st.text("Finished.")
        else:
            # TODO: Check if new comments and as if user wants to overwrite / run analysis
            st.text("Analysis for " + video1.get_car_name() + " / " + video1.get_channel_name() + " already exists.")
        videos_to_merge.append(video1)

        # Run analysis for video2
        if ((car2 != "") and (channel2 != "") and (url2 != "")):
            video2 = Video(car2, channel2, url2, feature_list)      
            if (not video2.content_exists()):
                st.text("Running analysis for " + video2.get_car_name() + " / " + video2.get_channel_name())
                st.text("1) Downloading content...")
                video2.get_content()
                st.text("2) Calculating sentiment...")
                video2.get_sentiment()
                st.text("3) Generating wordcloud...")
                video2.get_wordcloud()
                st.text("4) Calculating feature stats...")
                video2.get_feature_stats()
                st.text("Finished.")
            else:
                # TODO: Check if new comments and as if user wants to overwrite / run analysis
                st.text("Analysis for " + video2.get_car_name() + " / " + video2.get_channel_name() + " already exists.")
            videos_to_merge.append(video2)

        # Merge video1 and video2 if applicable and display
        merged_videos_path = app.merge_df(videos_to_merge) # TODO: Could also return df straight but getting weird errors because instance of Video class is EMPTY after changing elements below
        st.experimental_set_query_params(my_saved_result=merged_videos_path)  # Save value

# Retrieve app state
app_state = st.experimental_get_query_params()  
if "my_saved_result" in app_state:
    if "my_saved_result" in app_state:
        saved_result = app_state["my_saved_result"][0]
    else:
        st.write("No result to display, compute a value first.")

    # Read df 
    merged_videos = pd.read_csv(saved_result, header=[0], lineterminator='\n')

    st.markdown("""---""")
    app.space(1)
    st.subheader("Sentiment Radar Chart")
    st.caption("### View the sentiment of all mentioned features in a radar chart.")
    app.space(2)

    # Display videos that are in merged set
    all_videos = merged_videos["car"].unique().tolist()
    videos = st.multiselect("Select cars to visualize", all_videos, all_videos)
    app.space(1)

    # Display features that are in merged set
    all_features = merged_videos["feature"].unique().tolist()
    feature_list_visualize = st.multiselect("Select features to visualize", all_features, all_features)
    app.space(1)

    merged_videos = merged_videos[merged_videos["car"].isin(videos)]
    merged_videos = merged_videos[merged_videos["feature"].isin(feature_list_visualize)]
    app.radar_chart(merged_videos)         