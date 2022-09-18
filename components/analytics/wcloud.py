from utils import clean
from utils import sb
from utils import app
from components.analytics import helper
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import en_core_web_sm


# TODO: Select feature select box should only show features that are in content


def _get_df_feature_adj(df_feature):
    """
    Returns df with only adjectives in content
    """
    if "nlp" not in st.session_state:
        st.session_state["nlp"] = en_core_web_sm.load()
    nlp = st.session_state["nlp"]

    def _filter_adj_spacy(comment):
        comment = nlp(comment)
        return " ".join([token.text for token in comment if token.pos_ == "ADJ"])
    df_feature["content"] = df_feature["content"].apply(_filter_adj_spacy)
    return df_feature


def _generate_wordcloud(df):
    """
    Return wordcloud fig
    """
    @st.cache(suppress_st_warning=True)
    def _get_all_words(df):
        df = clean.basic_clean(df)
        df = clean.remove_stopwords(df)
        all_words = " ".join([w for w in df["content_no_stopwords"]])
        return all_words

    all_words = _get_all_words(df)

    wordcloud = WordCloud(width=900, height=500, random_state=21,
                          max_font_size=120).generate(all_words)
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig


def get_wordcloud():
    """
    Display wordcloud
    """
    cars = []
    for selected_video_id in st.session_state["video_ids_selected"]:
        cars.append(app.get_car_info(selected_video_id))

    selection_wordcloud = st.selectbox("Select car/video",
                                       cars)
    # TODO: Change this; text field should not display video_id; what if car name has "("? Use last bracket as input
    selected_video_id = re.search('\((.*?)\)', selection_wordcloud).group(1)

    feature = helper.get_list_of_all_features(selected_video_id)
    app.space(1)

    df = pd.DataFrame(sb.get_content(selected_video_id), columns=["content"])
    df_feature = helper.get_single_feature(df, feature)
    df_feature_adj = _get_df_feature_adj(df_feature)

    num_feature_mentions = len(df_feature)
    st.metric("Number of mentions", num_feature_mentions)
    app.space(2)

    if len(df_feature_adj) < 1:
        st.write(
            "This feature is not mentioned. Please try using a different feature.")
    else:
        st.pyplot(_generate_wordcloud(df_feature_adj))
