import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from components import header
from components import sentiment
from components import top_flop_features
from components import wcloud
from components.add_box import display_add_box
from components.edit_box import display_edit_box
from colour import Color
from database import db
from utils import app


def _display_sentiment(sentiment_data):
    """
    Display sentiment radar chart
    """
    st.plotly_chart(sentiment.get_radar_chart(sentiment_data),
                    use_container_width=True)


def _display_wcloud(df_feature_adj):
    """
    Display wordcloud
    """
    st.pyplot(wcloud.get_wordcloud(df_feature_adj))


def _display_topflop(cars, occurrence_cutoff):
    """
    Display top flop
    TODO: Top comments -- Add like count -- change 'video.py' while YT data is fetched
    """
    for make in st.session_state["cars"].keys():
        for model in st.session_state["cars"][make].keys():
            cars = {}
            cars[make] = {}
            cars[make][model] = st.session_state["cars"][make][model]
            df_car = top_flop_features.get_top_flop_features(cars)
            df_car = df_car.drop(
                df_car[df_car["comment_count"] < occurrence_cutoff].index)
            st.write("## {}".format(make + " " + model))

            if df_car.empty:
                st.warning("Not enough comments mention any feature")
            else:
                df_len = len(df_car)
                df_car_top = df_car
                df_car_flop = df_car.iloc[::-1]

                colors = list(Color("red").range_to(Color("green"), 6))

                st.write("##### Top 5 features")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                if df_len >= 1:
                    feature = df_car_top.iloc[0]["feature"].capitalize()
                    sentiment = round(df_car_top.iloc[0]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col1.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 2:
                    feature = df_car_top.iloc[1]["feature"].capitalize()
                    sentiment = round(df_car_top.iloc[1]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col2.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 3:
                    feature = df_car_top.iloc[2]["feature"].capitalize()
                    sentiment = round(df_car_top.iloc[2]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col3.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 4:
                    feature = df_car_top.iloc[3]["feature"].capitalize()
                    sentiment = round(df_car_top.iloc[3]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col4.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 5:
                    feature = df_car_top.iloc[4]["feature"].capitalize()
                    sentiment = round(df_car_top.iloc[4]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col5.markdown(html_str, unsafe_allow_html=True)

                st.write("##### Flop 5 features")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                if df_len >= 1:
                    feature = df_car_flop.iloc[0]["feature"].capitalize()
                    sentiment = round(df_car_flop.iloc[0]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col1.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 2:
                    feature = df_car_flop.iloc[1]["feature"].capitalize()
                    sentiment = round(df_car_flop.iloc[1]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col2.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 3:
                    feature = df_car_flop.iloc[2]["feature"].capitalize()
                    sentiment = round(df_car_flop.iloc[2]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col3.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 4:
                    feature = df_car_flop.iloc[3]["feature"].capitalize()
                    sentiment = round(df_car_flop.iloc[3]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col4.markdown(html_str, unsafe_allow_html=True)
                if df_len >= 5:
                    feature = df_car_flop.iloc[4]["feature"].capitalize()
                    sentiment = round(df_car_flop.iloc[4]["sentiment_mean"], 2)
                    color = colors[round(sentiment)]
                    html_str = f"<p style='color:{color}; margin-bottom: 0px; '>{feature}<h2 style='color:{color}; padding-top:0px'>{sentiment}</h2></p>"
                    col5.markdown(html_str, unsafe_allow_html=True)
            app.space(1)


@st.cache(suppress_st_warning=True)
def _get_feature_list(selected_car):
    """
    Return list of available features for selectbox,
    based on input of previous selectbox (`selected_video_id`)
    """
    # cars_unfiltered = st.session_state["cars"]
    # def dictfilt(x, y): return dict([(i, x[i]) for i in x if i in set(y)])

    # cars_filtered = dictfilt(cars_unfiltered, selected_car)
    # current = sb.get_feature_stats_for_cars(cars_filtered)

    current = db.get_feature_stats_for_cars(5)

    return sorted(current["feature"].to_list())


@st.cache(suppress_st_warning=True)
def _get_df(selected_car_id):
    """
    Return df with all features/sentiment entries
    """
    return pd.DataFrame(db.get_content_and_sentiment_for_car_id(selected_car_id),
                        columns=["content", "sentiment_score"])


def _get_df_feature(df, feature):
    """
    Return df with single selected feature
    """
    df = df[df["content"].notnull()]
    df_feature = pd.DataFrame()
    df_feature = pd.concat(
        [df_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
    df_feature["feature"] = feature
    return df_feature


# @st.cache(suppress_st_warning=True)
def _get_list_of_selected_cars_and_car_ids():
    """
    Return list of selected cars
    """
    cars = {}
    for make in st.session_state['cars'].keys():
        for model in st.session_state['cars'][make].keys():
            car_ids = []
            for car_id in st.session_state['cars'][make][model]:
                car_ids.append(car_id)
            cars[make + " " + model] = car_ids
    return cars


def display_menu_and_widgets():
    """
    Display menu along with its widgets
    """
    menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                       icons=['bar-chart-fill', 'type', 'star-half'],
                       menu_icon="cast", default_index=0, orientation="horizontal")

    if (menu == "Sentiment"):
        occurrence_cutoff = st.slider("Select how often a feature should be mentioned to appear",
                                      1, 100, key="occurrence_cutoff")
        st.success("Sentiment from 1 (negative) to 5 (postitive)")

        df_sentiment = sentiment.get_sentiment_data_for_cars(
            st.session_state['cars'], occurrence_cutoff)
        app.space(2)

        if not df_sentiment.empty:
            _display_sentiment(df_sentiment)
        else:
            st.warning("Not enough comments mention any feature")

    elif (menu == "Wordcloud"):
        cars = _get_list_of_selected_cars_and_car_ids()

        selected_car = st.selectbox(
            "Select car", cars.keys())
        selected_feature = st.selectbox(
            "Select feature", _get_feature_list(selected_car))

        df_w_tf_all = pd.DataFrame()
        for car_id in cars[selected_car]:
            df_w_tf_all = pd.concat([df_w_tf_all, _get_df(car_id)], axis=0)

        df_feature = _get_df_feature(df_w_tf_all, selected_feature)

        st.metric("Number of mentions", len(df_feature))
        app.space(1)

        df_feature_adj = wcloud.get_df_feature_adj(df_feature)
        # TODO: Re-check this, wordcloud does not print with only one word in `df_feature_adj`
        if len(df_feature_adj) <= 1:
            st.warning(
                "No comments mention this feature")
        else:
            _display_wcloud(df_feature_adj)

    elif (menu == "Top/Flop"):
        cars = _get_list_of_selected_cars_and_car_ids()

        occurrence_cutoff = st.slider("Select how often a feature should be mentioned to appear",
                                      1, 100, key="occurrence_cutoff")

        app.space(2)

        _display_topflop(cars, occurrence_cutoff)


def run():
    header.display()

    with open("style/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "cars" not in st.session_state:
        st.session_state["cars"] = {}

    print("Cars (Analytics):", st.session_state["cars"], "\n")

    if st.session_state["cars"]:
        display_menu_and_widgets()
        app.space(3)
        display_add_box("Compare with another car ➕ 🚗")
        display_edit_box()
    else:
        display_add_box("Add a car to get started ➕🚗")


if __name__ == "__main__":
    run()
