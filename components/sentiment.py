from utils import sb
from utils import app
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache(suppress_st_warning=True)
def get_radar_chart(df):
    """
    Return sentiment radar chart as fig
    """
    fig = px.line_polar(df,
                        r='sentiment_mean',
                        theta='feature',
                        color='car',
                        line_close=True,
                        line_shape='linear',  # or spline
                        hover_name='car',
                        hover_data={'car': False},
                        markers=True,
                        # labels={'rating': 'stars'},
                        # text='car',
                        # start_angle=0,
                        range_r=[0, 5],
                        direction='clockwise')  # or counterclockwise
    fig.update_traces(fill='toself')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=1
    ))
    return fig


@st.cache(suppress_st_warning=True)
def get_sentiment_data(video_ids_selected, occurrence_cutoff):
    """
    Return sentiment data
    """
    def _get_feature_stats(video_ids_selected):
        feature_stats = pd.DataFrame(
            columns=["feature", "comment_count", "sentiment_mean", "car"])
        for video_id in video_ids_selected:
            current = sb.get_feature_stats(video_id)
            current['car'] = app.get_car_info(video_id)
            feature_stats = pd.concat(
                [feature_stats, current]).sort_values(by=["feature", "car"])
            feature_stats.insert(0, 'car', feature_stats.pop('car'))
        return feature_stats
    feature_stats = _get_feature_stats(video_ids_selected)

    def _rm_occurrence_cutoff(feature_stats, occurrence_cutoff):
        return feature_stats.drop(feature_stats[feature_stats["comment_count"] < occurrence_cutoff].index)
    feature_stats = _rm_occurrence_cutoff(feature_stats, occurrence_cutoff)

    def _rm_uncommon_features(feature_stats):
        return feature_stats[feature_stats.groupby(
            'feature')['feature'].transform('size') > (len(video_ids_selected) - 1)]
    feature_stats = _rm_uncommon_features(feature_stats)

    return feature_stats
