import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import re
from components import header
from components import sentiment
from components import wcloud
from utils import app
from utils import sb


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


def _display_topflop(df_feature_top, df_feature_flop):
    """
    Display top flop
    """
    # TODO: Add like count -- need to change 'video.py' while YT data is fetched
    # TODO: Often sentiment is calculated wrong (e.g., irony) -- how to fix? Fix e.g., by not showing sentiment, just display top 5 but without sentiment score, maybe with like count tho
    # TODO: Change how number of comments is displayed

    def _display_content(df):
        """
        Display content
        """
        col1, col2, col3 = st.columns([1, 1, 5])
        col1.markdown("**Rank**")
        col2.markdown("**Sentiment**")
        col3.markdown("**Content**")
        for i in range(0, len(df["content"].values.tolist())):
            col1, col2, col3 = st.columns([1, 1, 5])
            col1.markdown(i+1)
            col2.markdown(df["sentiment_score"].values.tolist()[i])
            col3.markdown(df["content"].values.tolist()[i])

    st.subheader("Top 5 comments")
    _display_content(df_feature_top)
    app.space(1)

    st.subheader("Flop 5 comments")
    _display_content(df_feature_flop)


@st.cache(suppress_st_warning=True)
def _get_list_of_selected_cars(selected_video_ids):
    """
    Return list of selected cars for selectbox below menu
    """
    cars = []
    for video_id in selected_video_ids:
        cars.append(app.get_car_info(video_id))
    return cars


@st.cache(suppress_st_warning=True)
def _get_feature_list(selected_video_id):
    """
    Return list of available features for selectbox,
    based on input of previous selectbox (`selected_video_id`)
    """
    current = sb.get_feature_stats(selected_video_id)
    return sorted(current["feature"].to_list())


@st.cache(suppress_st_warning=True)
def _get_selected_video_id(selected_car):
    """
    Return `video_id` of selected car
    `video_id` needs to be extracted from string in selectbox `selected_car`
    """
    return re.search('\((.*?)\)', selected_car).group(1)


@st.cache(suppress_st_warning=True)
def _get_df(selected_video_id):
    """
    Return df with all features/sentiment entries
    """
    return pd.DataFrame(sb.get_content_and_sentiment(selected_video_id),
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


def _display_edit_box():
    """
    Display edit box
    """
    def _edit_box_header():
        """
        Display edit box header
        """
        col1, col2, col3, col4, col5, col6 = st.columns(
            [3.2, 1.2, 1.2, 1.2, 1.2, 1.2])

        col1.write("###### Car")
        col2.write("###### Channel")
        col3.write("###### Views")
        col4.write("###### Comments")
        col5.write("###### Video ID")
        col6.write("###### Remove?")

    def _edit_tile(video_id, meta):
        """
        Display edit tile for each video_id
        """
        # TODO: Cache this for all cars
        car_info = sb.get_car_from_video_id(video_id)

        col1, col2, col3, col4, col5, col6 = st.columns(
            [3.2, 1.2, 1.2, 1.2, 1.2, 1.2])

        col1.write("")
        col1.write(car_info["make"] + " " +
                   car_info["model"] + " (" +
                   car_info["trim"] + ", " +
                   str(car_info["year"]) + ")")

        col2.write("")
        col2.write(meta["channel_title"])

        col3.write("")
        col3.write(app.human_format(int(meta["view_count"])) + " views")

        col4.write("")
        col4.write(app.human_format(
            int(meta["comment_count"])) + " comments")

        col5.write("")
        col5.write(video_id)

        remove = col6.button('Remove', key=video_id + "_remove")
        if (remove and video_id in st.session_state['video_ids_selected']):
            st.session_state['video_ids_selected'].remove(video_id)
            st.experimental_rerun()

    if len(st.session_state['video_ids_selected']) > 0:
        with st.expander("Edit selection 🚗", expanded=True):
            app.space(1)
            _edit_box_header()
            app.space(1)
            for video_id in st.session_state['video_ids_selected']:
                _edit_tile(video_id, sb.get_meta(video_id))
            app.space(1)
            if st.button("Add another car to anaysis"):
                switch_page("select")
        app.space(1)


def _display_menu_and_widgets():
    """
    Display menu along with its widgets
    """
    menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                       icons=['bar-chart-fill', 'type', 'star-half'],
                       menu_icon="cast", default_index=0, orientation="horizontal")

    if (menu == "Sentiment"):
        occurrence_cutoff = st.slider("Select minimum munber of feature occurrences",
                                      1, 30, key="occurrence_cutoff")
        df_sentiment = sentiment.get_sentiment_data(st.session_state['video_ids_selected'],
                                                    occurrence_cutoff)
        _display_sentiment(df_sentiment)

    elif (menu == "Wordcloud" or menu == "Top/Flop"):
        selected_car = st.selectbox("Select car/video",
                                    _get_list_of_selected_cars(st.session_state["video_ids_selected"]))
        # TODO: Display wihtout video_id; Use last bracket as input (avoid issue if car name has `(`)
        selected_video_id = _get_selected_video_id(selected_car)
        selected_feature = st.selectbox("Select feature",
                                        _get_feature_list(selected_video_id))
        app.space(1)

        df_w_tf = _get_df(selected_video_id)
        df_feature = _get_df_feature(df_w_tf, selected_feature)

        st.metric("Number of mentions", len(df_feature))
        app.space(1)

        if (menu == "Wordcloud"):
            df_feature_adj = wcloud.get_df_feature_adj(df_feature)
            # TODO: Re-check this, wordcloud does not print with only one word in `df_feature_adj`
            if len(df_feature_adj) <= 1:
                st.warning(
                    "No adjectives were mentioned to describe this feature. Please select a different feature.")
            else:
                print(len(df_feature_adj))
                _display_wcloud(df_feature_adj)

        elif (menu == "Top/Flop"):
            df_feature_top = df_feature.iloc[-5:]
            df_feature_top = df_feature_top.iloc[::-1]
            df_feature_flop = df_feature.iloc[:5]
            _display_topflop(df_feature_top, df_feature_flop)


def run():
    header.display()
    if "video_ids_selected" not in st.session_state:
        st.session_state["video_ids_selected"] = []
    if st.session_state["video_ids_selected"]:
        _display_edit_box()
        _display_menu_and_widgets()
    else:
        st.warning("Please select a Car and Video to get started")


if __name__ == "__main__":
    run()
