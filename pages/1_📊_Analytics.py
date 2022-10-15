import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from components import header
from components import sentiment
from components.wcloud import get_wordcloud, get_df_feature_adj
from components import form
from utils import app
from database import db


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


def _display_add_box(label):
    """
    Display add box

    TODO: Display this when no car is in session state
    """
    def _update_session_state(car_id, make, model, previews):
        if model == previews["model"]:
            model = db.get_model_from_car_id(car_id)

        if make not in st.session_state["car_ids"]:
            st.session_state["car_ids"][make] = {}
        if model not in st.session_state["car_ids"][make]:
            st.session_state["car_ids"][make][model] = {}
        if car_id not in st.session_state["car_ids"][make][model]:
            st.session_state["car_ids"][make][model][car_id] = db.get_num_comments_for_car_id(
                car_id)
            return True
        else:
            return False
        # todo also add video ids on  car id, and then all comments per nvideo id.... b etter overview

    previews = form._get_previews()

    if "car_selected" not in st.session_state:
        st.session_state["car_selected"] = {
            "make": previews["make"],
            "model": previews["model"],
            "trim": previews["trim"],
            "year": previews["year"]
        }

    with st.expander(label, expanded=True):
        col1, col2 = st.columns([1, 1])

        makes = db.get_makes()
        makes.insert(0, previews["make"])
        make = col1.selectbox("Make", makes, key="make_selected")

        models = db.get_models(make)
        models.insert(0, previews["model"])
        model = col2.selectbox("Model", models)

        num_comments = app.human_format(
            db.get_num_comments_for_make_and_model(make, model))
        if num_comments == "0":
            num_comments = ""
        button = st.button("Analyze {} comments".format(num_comments))

        if button:
            def button(make, model):
                if (make == "" or make == previews["make"]):
                    st.warning("Please select a Make")
                else:
                    if model == previews["model"]:
                        # potentially multiple models

                        models = db.get_models_of_make(make)
                        if make not in st.session_state["cars"]:
                            st.session_state["cars"][make] = {}
                        for model in models:
                            if model not in st.session_state["cars"][make]:
                                st.session_state["cars"][make][model] = {}

                            car_ids = db.get_car_id_from_make_model(
                                make, model)
                            changes = False
                            changes = True  # figure  out where this should go
                            for car_id in car_ids:
                                if car_id not in st.session_state["cars"][make][model]:
                                    changes = True
                                    st.session_state["cars"][make][model][car_id] = {
                                    }

                                    video_ids = db.get_video_ids_for_car_id(
                                        car_id)
                                    for video_id in video_ids:
                                        if video_id not in st.session_state["cars"][make][model][car_id]:
                                            st.session_state["cars"][make][model][car_id][video_id] = db.get_comment_count_actual_for_video_id(
                                                video_id)
                    else:
                        if make not in st.session_state["cars"]:
                            st.session_state["cars"][make] = {}
                        if model not in st.session_state["cars"][make]:
                            st.session_state["cars"][make][model] = {}

                        car_ids = db.get_car_id_from_make_model(make, model)
                        changes = False
                        changes = True  # figure  out where this should go
                        for car_id in car_ids:
                            if car_id not in st.session_state["cars"][make][model]:
                                changes = True
                                st.session_state["cars"][make][model][car_id] = {
                                }

                                video_ids = db.get_video_ids_for_car_id(car_id)
                                for video_id in video_ids:
                                    if video_id not in st.session_state["cars"][make][model][car_id]:
                                        st.session_state["cars"][make][model][car_id][video_id] = db.get_comment_count_actual_for_video_id(
                                            video_id)
                    print("CARS: ", st.session_state["cars"])
                    return changes

            changes = button(make, model)

            if changes:
                st.experimental_rerun()


def _display_edit_box():
    """
    Display edit box
    """
    def _edit_tile(make, model, comment_count):
        """
        Display edit tile for each car_id
        """
        # TODO: Cache this for all cars
        col1, col2, col3 = st.columns(
            [2, 1, 1])

        col1.write("")
        col1.write("{} {}".format(make, model))

        col2.write("")
        col2.write(comment_count + " comments")

        # delete
        remove = col3.button('Remove', key=str(make + " " + model) + "_remove")
        if remove:
            if make in st.session_state['cars'].keys():
                if model in st.session_state['cars'][make].keys():
                    print("TODO: REMOVE ", make, model)
                    st.session_state['cars'][make].pop(model)
                if len(st.session_state['cars'][make].keys()) == 0:
                    st.session_state['cars'].pop(make)
            st.experimental_rerun()
        # if (remove and car_id in st.session_state["car_ids"][make][model]):
        #     st.session_state['car_ids_selected'].remove(car_id)
        #     print(st.session_state['car_ids_selected'])
        #     st.experimental_rerun()

            # if car_id not in st.session_state["car_ids"][make][model]:
            # st.session_state["car_ids"][make][model][car_id] = sb.get_num_comments_for_car_id(
            #     car_id)

    if len(st.session_state["cars"]) > 0:
        with st.expander("Edit selection ⚙️ 🚗", expanded=True):
            for make in st.session_state['cars'].keys():
                for model in st.session_state['cars'][make].keys():
                    _edit_tile(
                        make,
                        model,
                        app.human_format(db.get_num_comments_for_make_and_model(make, model)))


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
        st.success("Sentiment from 1 (negative) to 5 (postitive)")

        df_sentiment = sentiment.get_sentiment_data_for_cars(
            st.session_state['cars'], occurrence_cutoff)
        app.space(2)

        if not df_sentiment.empty:
            _display_sentiment(df_sentiment)
        else:
            st.warning("Not enough comments mention any feature")

    elif (menu == "Wordcloud" or menu == "Top/Flop"):
        cars = {}
        for make in st.session_state['cars'].keys():
            for model in st.session_state['cars'][make].keys():
                car_ids = []
                for car_id in st.session_state['cars'][make][model]:
                    car_ids.append(car_id)
                cars[make + " " + model] = car_ids
        print(cars)

        selected_car = st.selectbox("Select car", cars.keys())

        selected_feature = st.selectbox("Select feature",
                                        _get_feature_list(selected_car))

        df_w_tf_all = pd.DataFrame()
        for car_id in cars[selected_car]:
            df_w_tf_all = pd.concat([df_w_tf_all, _get_df(car_id)], axis=0)

        print(df_w_tf_all)
        df_feature = _get_df_feature(df_w_tf_all, selected_feature)

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
    print(st.session_state["cars"])
    header.display()

    with open("style/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "cars" not in st.session_state:
        st.session_state["cars"] = {}

    if st.session_state["cars"]:
        _display_menu_and_widgets()
        app.space(3)
        _display_add_box("Compare with another car ➕ 🚗")
        _display_edit_box()
    else:
        _display_add_box("Add a car to get started ➕🚗")


if __name__ == "__main__":
    run()
