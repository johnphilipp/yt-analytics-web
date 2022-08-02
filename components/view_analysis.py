from utils import clean
from utils import sb
from utils import app
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import io
import re


# -----------------------------------------------------------------------

# Get car info from video_id
def _get_car_info(video_id):
    car_info = sb.get_car_from_video_id(video_id)
    car_info_string = car_info["make"] + " " + \
        car_info["model"] + " " + \
        car_info["trim"] + " " + \
        str(car_info["year"]) + " (" + \
        video_id + ")"
    return car_info_string

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
        yanchor="top",
        y=-0.15,
        xanchor="left",
        x=0.15
    ))
    st.write(fig)


# -----------------------------------------------------------------------

# Generate and display wordcloud

def _get_wordcloud(df):
    df = clean.basic_clean(df)
    df = clean.remove_stopwords(df)
    all_words = " ".join([w for w in df["content_no_stopwords"]])
    wordcloud = WordCloud(width=500, height=300, random_state=21,
                          max_font_size=119).generate(all_words)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')

    st.image(img_buf)


# -----------------------------------------------------------------------

# Main body: View Analysis

def view_analysis():
    if len(st.session_state['video_ids_selected']) > 0:
        st.markdown("---")
        app.space(2)
        st.subheader("View Analysis 📊")
        app.space(2)

        menu = option_menu(None, ["Sentiment", "Wordcloud"],
                           icons=['bar-chart', 'type'],
                           menu_icon="cast", default_index=0, orientation="horizontal")

        if menu == "Sentiment":
            def get_feature_stats():
                feature_stats = pd.DataFrame(
                    columns=["feature", "comment_count", "sentiment_mean", "car"])
                for video_id in st.session_state['video_ids_selected']:
                    current = sb.get_feature_stats(video_id)
                    current['car'] = _get_car_info(video_id)
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

        elif menu == "Wordcloud":
            cars = []
            for selected_video_id in st.session_state['video_ids_selected']:
                cars.append(_get_car_info(selected_video_id))

            selection_wordcloud = st.selectbox(
                'Edit selection', cars)

            selected_video_id = re.search(
                '\((.*?)\)', selection_wordcloud).group(1)

            df = pd.DataFrame(sb.get_content(
                selected_video_id), columns=['content'])

            _get_wordcloud(df)
