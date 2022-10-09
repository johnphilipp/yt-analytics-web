import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import re
from components import header
from components import sentiment
from components.wcloud import get_wordcloud, get_df_feature_adj
from components import form
from utils import app
from utils import sb
from utils import switch_page


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
    st.pyplot(get_wordcloud(df_feature_adj))


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
def _get_feature_list(car_id_selected):
    """
    Return list of available features for selectbox,
    based on input of previous selectbox (`selected_video_id`)
    """
    current = sb.get_feature_stats_for_car_id(car_id_selected)
    return sorted(current["feature"].to_list())


@st.cache(suppress_st_warning=True)
def _get_df(selected_car_id):
    """
    Return df with all features/sentiment entries
    """
    return pd.DataFrame(sb.get_content_and_sentiment_for_car_id(selected_car_id),
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


def _display_add_box():
    """
    Display add box

    TODO: Display this when no car is in session state
    """
    if len(st.session_state['car_selected']) > 0:
        previews = form._get_previews()

        if "car_selected" not in st.session_state:
            st.session_state["car_selected"] = {
                "make": previews["make"],
                "model": previews["model"],
                "trim": previews["trim"],
                "year": previews["year"]
            }

        with st.expander("Compare with another car ➕ 🚗", expanded=True):
            col1, col2 = st.columns([1, 1])

            makes = sb.get_makes()
            makes.insert(0, previews["make"])
            make = col1.selectbox("Make", makes, key="make_selected")

            models = sb.get_models(make)
            models.insert(0, previews["model"])
            model = col2.selectbox("Model", models)

            button = st.button("Analyze {} comments".format(
                form.get_button_num_comments(make, model, previews)))

            if button:
                if (make == "" or make == previews["make"]):
                    st.warning("Please select a Make")
                else:
                    selected_cars = form.get_car_ids(make, model, previews)
                    if isinstance(selected_cars, int):
                        car = selected_cars
                        if car not in st.session_state["car_ids_selected"]:
                            st.session_state["car_ids_selected"].append(car)
                            st.experimental_rerun()
                    else:
                        for car in selected_cars:
                            if car not in st.session_state["car_ids_selected"]:
                                st.session_state["car_ids_selected"].append(
                                    car)
                            st.experimental_rerun()


def _display_edit_box():
    """
    Display edit box
    """
    def _edit_tile(car_id, comment_count):
        """
        Display edit tile for each car_id
        """
        # TODO: Cache this for all cars
        car_info = sb.get_car_from_car_id(car_id)

        col1, col2, col3 = st.columns(
            [2, 1, 1])

        col1.write("")
        col1.write("{} {}".format(car_info["make"], car_info["model"]))

        col2.write("")
        col2.write(app.human_format(comment_count) + " comments")

        remove = col3.button('Remove', key=str(car_id) + "_remove")
        if (remove and car_id in st.session_state['car_ids_selected']):
            st.session_state['car_ids_selected'].remove(car_id)
            st.experimental_rerun()

    if len(st.session_state['car_ids_selected']) > 0:
        with st.expander("Edit selection ⚙️ 🚗", expanded=True):
            for car_id in st.session_state['car_ids_selected']:
                _edit_tile(car_id, sb.get_num_comments_for_car_id(car_id))


@st.cache(suppress_st_warning=True)
def _get_list_of_selected_cars(selected_car_ids):
    """
    Return list of selected cars for selectbox below menu
    """
    cars = []
    for car_id in selected_car_ids:
        cars.append(app.get_car_info_from_car_id(car_id))
    return cars


def _display_menu_and_widgets():
    """
    Display menu along with its widgets
    """
    menu = option_menu(None, ["Sentiment", "Wordcloud", "Top/Flop"],
                       icons=['bar-chart-fill', 'type', 'star-half'],
                       menu_icon="cast", default_index=0, orientation="horizontal")

    if (menu == "Sentiment"):
        occurrence_cutoff = st.slider("Select how often a feature needs to be mentioned to appear",
                                      1, 30, key="occurrence_cutoff")
        st.success(
            "Sentiment from 1 (negative) to 5 (postitive)")
        df_sentiment = sentiment.get_sentiment_data(st.session_state['car_ids_selected'],
                                                    occurrence_cutoff)
        _display_sentiment(df_sentiment)

    elif (menu == "Wordcloud" or menu == "Top/Flop"):
        # TODO

        display = _get_list_of_selected_cars(
            st.session_state["car_ids_selected"])

        if isinstance(st.session_state["car_ids_selected"], int):
            options = st.session_state["car_ids_selected"]
            car_id_selected = st.selectbox(
                "gender", options, format_func=lambda x: display[0])
        else:
            options = st.session_state["car_ids_selected"]
            car_id_selected = st.selectbox(
                "gender", options, format_func=lambda x: display[options.index(x)])

        selected_feature = st.selectbox("Select feature",
                                        _get_feature_list(car_id_selected))
        app.space(1)

        df_w_tf = _get_df(car_id_selected)
        df_feature = _get_df_feature(df_w_tf, selected_feature)

        st.metric("Number of mentions", len(df_feature))
        app.space(1)

        if (menu == "Wordcloud"):
            df_feature_adj = get_df_feature_adj(df_feature)
            # TODO: Re-check this, wordcloud does not print with only one word in `df_feature_adj`
            if len(df_feature_adj) <= 1:
                st.warning(
                    "No adjectives were mentioned to describe this feature. Please select a different feature.")
            else:
                _display_wcloud(df_feature_adj)

        elif (menu == "Top/Flop"):
            df_feature_top = df_feature.iloc[-5:]
            df_feature_top = df_feature_top.iloc[::-1]
            df_feature_flop = df_feature.iloc[:5]
            _display_topflop(df_feature_top, df_feature_flop)


def run():
    header.display()

    with open("style/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "car_ids_selected" not in st.session_state:
        st.session_state["car_ids_selected"] = []

    if st.session_state["car_ids_selected"]:
        _display_menu_and_widgets()
        app.space(3)
        _display_add_box()
        _display_edit_box()
    else:
        st.warning("Please select a Car and Video to get started")


if __name__ == "__main__":
    run()
