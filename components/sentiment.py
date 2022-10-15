from database import db
from utils import app
import streamlit as st
import pandas as pd
import plotly.express as px


# @st.cache(suppress_st_warning=True)
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
                        hover_name='make',
                        hover_data={'make': False},
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


def get_sentiment_data_for_cars(cars, occurrence_cutoff=1):
    """
    Return sentiment data
    """
    feature_stats = db.get_feature_stats_for_cars(cars)

    def _rm_occurrence_cutoff(feature_stats, occurrence_cutoff):
        return feature_stats.drop(feature_stats[feature_stats["comment_count"] < occurrence_cutoff].index)
    feature_stats = _rm_occurrence_cutoff(feature_stats, occurrence_cutoff)

    def _rm_uncommon_features(feature_stats):
        length = 0
        for make in cars.keys():
            length += len(cars[make].keys())
        feature_stats = feature_stats[feature_stats.groupby(
            'feature')['feature'].transform('size') > length - 1]  # TODO
        return feature_stats
    feature_stats = _rm_uncommon_features(feature_stats)

    return feature_stats
