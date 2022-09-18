import streamlit as st
from utils import sb
import pandas as pd


def get_single_feature(df, feature):
    """
    Returns df of a single feature for a video_id
    """
    df = df[df["content"].notnull()]
    df_single_feature = pd.DataFrame()
    df_single_feature = pd.concat(
        [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
    df_single_feature["feature"] = feature
    return df_single_feature


def get_list_of_all_features(selected_video_id):
    """
    Display feature selectbox
    """
    @st.cache(suppress_st_warning=True)
    def _get_feature_list(video_id):
        """
        Return list with available features for selectbox 
        based on selected video_id
        """
        current = sb.get_feature_stats(video_id)
        return sorted(current["feature"].to_list())

    feature_list = _get_feature_list(selected_video_id)
    feature = st.selectbox("Select feature", feature_list)
    return feature
