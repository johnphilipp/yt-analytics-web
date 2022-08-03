from utils import clean
from utils import sb
from utils import app
from utils import features
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import re
import spacy


# -----------------------------------------------------------------------

# Helper func -- Returns df of a single feature

def _get_single_feature(df, feature):
    df = df[df["content"].notnull()]
    df_single_feature = pd.DataFrame()
    df_single_feature = pd.concat(
        [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
    df_single_feature["feature"] = feature
    return df_single_feature


# -----------------------------------------------------------------------

# Main func -- Generate and display top flop comments

def get_topflop():
    # Display selectbox for car/video
    cars = []
    for selected_video_id in st.session_state["video_ids_selected"]:
        cars.append(app.get_car_info(selected_video_id))
    selection_wordcloud = st.selectbox(
        "Select car/video", cars)

    # Display selectbox for feature
    feature = st.selectbox(
        "Select feature", features.get_defined_feature_list())

    # Get df with content that only includes mention of feature + only keep adjectives
    selected_video_id = re.search(
        '\((.*?)\)', selection_wordcloud).group(1)  # TODO: Change this; text field should not display video_id; what if car name has "("? Use last bracket as input
    df = pd.DataFrame(sb.get_content_and_sentiment(
        selected_video_id), columns=["content", "sentiment_score"])
    df_feature = _get_single_feature(
        df, feature).sort_values(by=["sentiment_score"])
    df_feature_top = df_feature.iloc[-5:]
    df_feature_flop = df_feature.iloc[:5]

    app.space(1)

    st.subheader("Number of feature mentions: " + str(len(df_feature)))

    app.space(1)

    st.subheader("Top 5 comments")
    col1, col2, col3 = st.columns([1, 1, 5])
    col1.markdown("**Rank**")
    col2.markdown("**Sentiment**")
    col3.markdown("**Content**")
    # TODO: Reverse list
    for i in range(0, len(df_feature_top["content"].values.tolist())):
        col1, col2, col3 = st.columns([1, 1, 5])
        col1.markdown(i)
        col2.markdown(
            df_feature_top["sentiment_score"].values.tolist()[i])
        col3.markdown(
            df_feature_top["content"].values.tolist()[i])

    app.space(1)

    st.subheader("Flop 5 comments")
    col1, col2, col3 = st.columns([1, 1, 5])
    col1.markdown("**Rank**")
    col2.markdown("**Sentiment**")
    col3.markdown("**Content**")
    for i in range(0, len(df_feature_flop["content"].values.tolist())):
        col1, col2, col3 = st.columns([0.2, 0.2, 5])
        col1.markdown(i)
        col2.markdown(df_feature_flop["sentiment_score"].values.tolist()[i])
        col3.markdown(df_feature_flop["content"].values.tolist()[i])
