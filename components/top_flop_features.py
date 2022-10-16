from database import db
import pandas as pd
import streamlit as st


@st.cache(suppress_st_warning=True)
def get_top_flop_features(cars):
    """
    Return df of top features for car
    Input, e.g.:
    {'Porsche': 
        {'Taycan': 
            {5: {'0vq6KEOIiMg': 3779}, 
            6: {'YvjsGHLORuo': 1206, 
                '7t7yZzd5IHA': 484}, 
            7: {'BAZX9p2oGOg': 3936}, 
            10: {'tdlmcqlVnjo': 209}, 
            11: {'IExib0QwWuA': 312}, 
            12: {'6oVwtI0k-xg': 1281}}}}
    """

    df_car = db.get_feature_stats_for_cars(cars)

    df_car = df_car.sort_values(by=["sentiment_mean"], ascending=False)

    return df_car
