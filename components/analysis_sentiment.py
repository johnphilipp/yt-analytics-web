from utils import sb
from utils import app
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px


# -----------------------------------------------------------------------

# Helper func -- Generatenmb and display sentiment radar chart

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
        yanchor="top",
        y=-0.15,
        xanchor="left",
        x=0.15
    ))
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------

# Main func -- Get sentiment

def get_sentiment():
    def get_feature_stats():
        feature_stats = pd.DataFrame(
            columns=["feature", "comment_count", "sentiment_mean", "car"])
        for video_id in st.session_state['video_ids_selected']:
            current = sb.get_feature_stats(video_id)
            current['car'] = app.get_car_info(video_id)
            feature_stats = pd.concat(
                [feature_stats, current]).sort_values(by=["feature", "car"])
            feature_stats.insert(0, 'car', feature_stats.pop('car'))
        return feature_stats

    feature_stats = get_feature_stats()
    feature_stats = feature_stats[feature_stats.groupby(
        'feature')['feature'].transform('size') > (len(st.session_state['video_ids_selected']) - 1)]

    # Display radar chart
    _get_radar_chart(feature_stats)

    # # Display features that are in merged set
    # all_features = feature_stats["feature"].unique().tolist()
    # st.multiselect("Edit features to visualize",
    #                all_features, all_features)
    # app.space(1)
