import streamlit as st
import plotly.express as px
import pandas as pd
import os
from pathlib import Path

#-----------------------------------------------------------------------

# https://github.com/streamlit/example-app-commenting/blob/main/utils/chart.py
# https://share.streamlit.io/streamlit/example-app-commenting/main

#-----------------------------------------------------------------------

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def display_video_data(video_id, video_data, key):
    col1, col2, col3 = st.columns([0.14, 1, 2.2])
    col2.image(video_data["thumbnail_url"], width=200)
    col3.text(video_data["title"])
    col3.text(video_data["channel"] + " ・ " + str(video_data["date_released"]) + " ・ " + human_format(int(video_data["num_comments"])) + " comments ・ " + human_format(int(video_data["num_views"])) + " views")
    
    # TODO: Very buggy, need to fix; checkmark pops back 
    def _checkbox_preset_checker():
        return video_id in st.session_state['video_ids_selected']
    col1.markdown("<a style='top: 50px;'>&nbsp;</a>", unsafe_allow_html=True)
    selected = col1.checkbox('', value=_checkbox_preset_checker(), key=video_id + key)\

    # Keep track of elements in list
    if selected and video_id not in st.session_state['video_ids_selected']:
        print("DEBUG 3")
        st.session_state['video_ids_selected'].append(video_id)
    elif not selected and video_id in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].remove(video_id)
        print("DEBUG 4")
    print(st.session_state['video_ids_selected'])

#-----------------------------------------------------------------------

def merge_df(videos):
    # Get and merge dfs
    print("")
    print("DEBUG: Merge df in app2.py")
    print(videos)
    print("")

    df = pd.DataFrame()
    for video in videos:
        df_video = pd.read_csv(video.get_dir() + "/feature_stats.csv", lineterminator='\n')
        df_video = df_video.drop(['Unnamed: 0'], axis=1, errors='ignore')
        df_video['car'] = video.get_car_name()
        df_video['channel'] = video.get_channel_name()
        df = pd.concat([df, df_video])

    df = df.reset_index(drop=True)
    df = df[df.groupby('feature')["feature"].transform(len) > (len(videos) - 1)]
    df = df.sort_values(by=['feature'])
    df.insert(0, 'car', df.pop('car'))
    df.insert(1, 'channel', df.pop('channel'))

    # Write df
    id = 0
    found = False
    main_dir = os.path.dirname(__file__)
    merge_dir = os.path.join(main_dir, "../data/#merge")
    while (found == False):
        path = Path(merge_dir + "/" + str(id) + ".csv")
        if (path.is_file()):
            id += 1
        else:
            df.to_csv(merge_dir + "/" + str(id) + ".csv") 
            found = True

    return path

#-----------------------------------------------------------------------

def radar_chart(df):  
    fig = px.line_polar(df, 
                        r='sentiment_mean', 
                        theta='feature', 
                        color='car', 
                        line_close=True,
                        line_shape='linear',  # or spline
                        hover_name='car',
                        hover_data={'car':False},
                        markers=True,
                        # labels={'rating':'stars'},
                        # text='car',
                        # start_angle=0,
                        range_r=[0,5],
                        direction='clockwise')  # or counterclockwise
    fig.update_traces(fill='toself')
    st.write(fig)

#-----------------------------------------------------------------------

def main():
    st.set_page_config(layout="centered", page_icon="🚗", page_title="YouTube Comment Analyzer")

    st.title("🚗 YouTube Comment Analyzer 📊")

    space(2)

    cars = ["Porsche_911_GT3__Porsche",
            "Porsche_911_Sport_Classic​__Porsche",
            "Porsche_911_GT3__Carfection",
            "Porsche_911_GT3__carwow",
            "Porsche_911_GT3_Touring__Collecting_Cars"
            ]
    source = merge_df(cars)
    all_models = source["car"].unique().tolist()
    models = st.multiselect("Choose models to visualize", all_models, all_models[:2])

    space(1)

    all_features = source["feature"].unique().tolist()
    features = st.multiselect("Choose features to visualize", all_features, all_features[:5])

    space(1)

    source = source[source["car"].isin(models)]
    source = source[source["feature"].isin(features)]
    radar_chart(source)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()