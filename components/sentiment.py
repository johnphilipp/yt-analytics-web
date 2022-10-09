from utils import sb
from utils import app
import streamlit as st
import pandas as pd
import plotly.express as px


# @st.cache(suppress_st_warning=True)
def get_radar_chart(df):
    """
    Return sentiment radar chart as fig
    """
    print(df.head())
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

    # import plotly.graph_objects as go
    # import numpy as np
    # import pandas as pd

    # # categories:
    # categories = ['processing cost', 'mechanical properties', 'chemical stability',
    #               'thermal stability', 'device integration']

    # # values:
    # rVars1 = [1, 5, 2, 2, 3]
    # rVars2 = [4, 3, 2.5, 1, 2]

    # rAllMax = max(rVars1+rVars2)

    # # colors
    # values = [1, 1, 1, 1, 1]
    # colors = ['rgba(216, 49, 49, 1)',
    #           'rgba(173, 87, 63, 1)',
    #           'rgba(130, 125, 76, 1)',
    #           'rgba(87, 163, 89, 1)',
    #           'rgba(44, 201, 102, 1)']

    # # some calcultations to place all elements
    # slices = len(rVars1)
    # fields = [max(rVars1)]*slices
    # circle_split = [360/slices]*(slices)
    # theta = 0
    # thetas = [0]
    # for t in circle_split:
    #     theta = theta+t
    #     thetas.append(theta)
    # thetas

    # # set up label positions
    # df_theta = pd.DataFrame({'theta': thetas, 'positions': ['middle right', 'middle right',
    #                                                         'bottom center', 'middle left',
    #                                                         'middle left', 'middle left']})

    # # plotly
    # fig = go.Figure()

    # # "background"
    # for t in range(0, len(colors)):
    #     fig.add_trace(go.Barpolar(
    #         r=[values[t]],
    #         width=360,
    #         marker_color=[colors[t]],
    #         opacity=0.6,
    #         name='Range ' + str(t+1)
    #         # showlegend=False,
    #     ))
    #     t = t+1

    # for r, cat in enumerate(categories):
    #     #print(r, cat)
    #     fig.add_trace(go.Scatterpolar(
    #         text=cat,
    #         r=[rAllMax],
    #         theta=[thetas[r]],
    #         mode='lines+text+markers',
    #         fill='toself',
    #         fillcolor='rgba(255, 255, 255, 0.4)',
    #         line=dict(color='black'),
    #         #textposition='bottom center',
    #         textposition=df_theta[df_theta['theta']
    #                               == thetas[r]]['positions'].values[0],
    #         marker=dict(line_color='white', color='black'),
    #         marker_symbol='circle',
    #         name=cat,
    #         showlegend=False))

    # # trace 1
    # fig.add_trace(go.Scatterpolar(
    #     #text = categories,
    #     r=rVars1,
    #     mode='lines+text+markers',
    #     fill='toself',
    #     fillcolor='rgba(0, 0, 255, 0.4)',
    #     textposition='bottom center',
    #     marker=dict(color='blue'),
    #     marker_symbol='square',
    #     name='Product A'))

    # # trace 2
    # fig.add_trace(go.Scatterpolar(
    #     #text = categories,
    #     r=rVars2,
    #     mode='lines+text+markers',
    #     fill='toself',
    #     fillcolor='rgba(0, 255, 0, 0.4)',
    #     textposition='bottom center',
    #     marker=dict(color='Green'),
    #     name='Product B'))

    # # adjust layout
    # fig.update_layout(
    #     template=None,
    #     polar=dict(radialaxis=dict(gridwidth=0.5,
    #                                range=[0, max(fields)],
    #                                showticklabels=True, ticks='', gridcolor="grey"),
    #                angularaxis=dict(showticklabels=False, ticks='',
    #                                 rotation=45,
    #                                 direction="clockwise",
    #                                 gridcolor="white")))

    # fig.update_yaxes(showline=True, linewidth=2, linecolor='white')

    return fig


# @st.cache(suppress_st_warning=True)
def get_sentiment_data(car_ids_selected, occurrence_cutoff):
    """
    Return sentiment data

    TODO: Stick dfs together; currently multiple entiures per feature for every video id
    """
    def _get_feature_stats(car_ids_selected):
        feature_stats = pd.DataFrame(
            columns=["feature", "comment_count", "sentiment_mean", "car"])
        for car_id in car_ids_selected:
            current = sb.get_feature_stats_for_car_id(car_id)
            print("current: ", current)
            current['car'] = app.get_car_make_and_model_from_car_id(car_id)
            feature_stats = pd.concat(
                [feature_stats, current]).sort_values(by=["feature", "car"])
            feature_stats.insert(0, 'car', feature_stats.pop('car'))
        return feature_stats
    feature_stats = _get_feature_stats(car_ids_selected)

    def _rm_occurrence_cutoff(feature_stats, occurrence_cutoff):
        return feature_stats.drop(feature_stats[feature_stats["comment_count"] < occurrence_cutoff].index)
    feature_stats = _rm_occurrence_cutoff(feature_stats, occurrence_cutoff)

    def _rm_uncommon_features(feature_stats):
        return feature_stats[feature_stats.groupby(
            'feature')['feature'].transform('size') > (len(car_ids_selected) - 1)]
    feature_stats = _rm_uncommon_features(feature_stats)

    return feature_stats
