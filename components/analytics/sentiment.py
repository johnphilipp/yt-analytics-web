from utils import sb
from utils import app
import streamlit as st
import pandas as pd
import plotly.express as px

#
# TODO: Add slider to select how many comments minimum (default 5)
#


# -----------------------------------------------------------------------

# Generate and display sentiment radar chart

def _get_radar_chart(df):
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
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------

# Get sentiment data

def _get_sentiment_data(video_ids_selected, occurrence_cutoff):
    @st.cache(suppress_st_warning=True)
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

    @st.cache(suppress_st_warning=True)
    def _rm_occurrence_cutoff(feature_stats, occurrence_cutoff):
        return feature_stats.drop(feature_stats[feature_stats["comment_count"] < occurrence_cutoff].index)
    feature_stats = _rm_occurrence_cutoff(feature_stats, occurrence_cutoff)

    @st.cache(suppress_st_warning=True)
    def _rm_uncommon_features(feature_stats):
        return feature_stats[feature_stats.groupby(
            'feature')['feature'].transform('size') > (len(video_ids_selected) - 1)]
    feature_stats = _rm_uncommon_features(feature_stats)

    print(feature_stats)
    return feature_stats

    # # Display features that are in merged set
    # all_features = feature_stats["feature"].unique().tolist()
    # st.multiselect("Edit features to visualize",
    #                all_features, all_features)
    # app.space(1)


# -----------------------------------------------------------------------

# Build plot

def get_sentiment_radar(video_ids_selected, occurrence_cutoff):
    sentiment_data = _get_sentiment_data(video_ids_selected, occurrence_cutoff)
    _get_radar_chart(sentiment_data)
