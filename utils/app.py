import streamlit as st
import plotly.express as px
import pandas as pd
from utils import sb

# -----------------------------------------------------------------------

# https://github.com/streamlit/example-app-commenting/blob/main/utils/chart.py
# https://share.streamlit.io/streamlit/example-app-commenting/main

# -----------------------------------------------------------------------


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def space_sidebar(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.sidebar.write("")


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def display_select(video_id, meta):
    col1, col2, col3, col4, col5 = st.columns([0.5, 2, 2.2, 1.1, 1.1])
    col2.image(meta["thumbnail_url"], width=180)
    col3.metric(label="Channel", value=meta["channel_title"])
    col4.metric(label="Views", value=human_format(int(meta["view_count"])))
    col5.metric(label="Comments", value=human_format(
        int(meta["comment_count"])))
    col1.header("")
    selected = col1.button('+', key=video_id + "_add")
    # Add selected videos to list
    if selected and video_id not in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].append(video_id)


def display_edit(video_id, meta):
    col1, col2, col3, col4, col5 = st.columns([0.6, 3.2, 1.2, 1.2, 1.2])

    col2.text(sb.get_car_from_video_id(video_id, "make") + " " +
              sb.get_car_from_video_id(video_id, "model") + " (" +
              sb.get_car_from_video_id(video_id, "trim") + ", " +
              str(sb.get_car_from_video_id(video_id, "year")) + ")")
    col3.text(meta["channel_title"])
    col4.text(human_format(int(meta["view_count"])) + " views")
    col5.text(human_format(int(meta["comment_count"])) + " comments")
    selected = col1.button('-', key=video_id + "_remove")
    # Remove selected videos from list
    if selected and video_id in st.session_state['video_ids_selected']:
        st.session_state['video_ids_selected'].remove(video_id)
        print("Removing ", sb.get_car_from_video_id(video_id))
        print("Button ", selected)

# -----------------------------------------------------------------------


def merge_df(videos):
    # Get and merge dfs
    print("")
    print("DEBUG: Merge df in app2.py")
    print(videos)
    print("")

    df = pd.DataFrame()
    for video in videos:
        df_video = pd.read_csv(
            video.get_dir() + "/feature_stats.csv", lineterminator='\n')
        df_video = df_video.drop(['Unnamed: 0'], axis=1, errors='ignore')
        df_video['car'] = video.get_car_name()
        df_video['channel'] = video.get_channel_name()
        df = pd.concat([df, df_video])

    df = df.reset_index(drop=True)
    df = df[df.groupby('feature')["feature"].transform(len)
            > (len(videos) - 1)]
    df = df.sort_values(by=['feature'])
    df.insert(0, 'car', df.pop('car'))
    df.insert(1, 'channel', df.pop('channel'))


# -----------------------------------------------------------------------


def radar_chart(df):
    fig = px.line_polar(df,
                        r='sentiment_mean',
                        theta='feature',
                        color='car',
                        line_close=True,
                        line_shape='linear',  # or spline
                        hover_name='car',
                        hover_data={'car': False},
                        markers=True,
                        # labels={'rating':'stars'},
                        # text='car',
                        # start_angle=0,
                        range_r=[0, 5],
                        direction='clockwise')  # or counterclockwise
    fig.update_traces(fill='toself')
    st.write(fig)

# -----------------------------------------------------------------------


def main():
    st.set_page_config(layout="centered", page_icon="🚗",
                       page_title="YouTube Comment Analyzer")

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
    models = st.multiselect("Choose models to visualize",
                            all_models, all_models[:2])

    space(1)

    all_features = source["feature"].unique().tolist()
    features = st.multiselect(
        "Choose features to visualize", all_features, all_features[:5])

    space(1)

    source = source[source["car"].isin(models)]
    source = source[source["feature"].isin(features)]
    radar_chart(source)

# -----------------------------------------------------------------------


if __name__ == '__main__':
    main()
