from utils import clean
from utils import sb
from utils import app
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import en_core_web_sm


# TODO: Select feature select box should only show features that are in content


# -----------------------------------------------------------------------

# Get df with content that only includes mention of feature + only keep adjectives

def _get_df_feature_adj(selected_video_id, feature):
    df = pd.DataFrame(sb.get_content(
        selected_video_id), columns=["content"])

    # Returns df of a single feature
    @st.cache(suppress_st_warning=True)
    def _get_single_feature(df, feature):
        df = df[df["content"].notnull()]
        df_single_feature = pd.DataFrame()
        df_single_feature = pd.concat(
            [df_single_feature, df[df["content"].str.lower().str.contains(feature)]], axis=0)
        df_single_feature["feature"] = feature
        return df_single_feature
    df_feature = _get_single_feature(df, feature)

    # Returns df with only adjectives in content
    @st.cache(suppress_st_warning=True)
    def _get_adj(df):
        if "nlp" not in st.session_state:
            st.session_state["nlp"] = en_core_web_sm.load()
        nlp = st.session_state["nlp"]

        def _filter_adj_spacy(comment):
            comment = nlp(comment)
            return " ".join([token.text for token in comment if token.pos_ == "ADJ"])
        df["content"] = df["content"].apply(_filter_adj_spacy)
        return df
    df_feature_adj = _get_adj(df_feature)

    return df_feature_adj


# -----------------------------------------------------------------------

# Generate and display wordcloud

def _generate_wordcloud(df):
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
    st.pyplot(fig)


# -----------------------------------------------------------------------

# Generate and display wordcloud

def get_wordcloud():
    cars = []
    for selected_video_id in st.session_state["video_ids_selected"]:
        cars.append(app.get_car_info(selected_video_id))

    selection_wordcloud = st.selectbox("Select car/video",
                                       cars)
    feature = st.selectbox("Select feature",
                           app.get_defined_feature_list())
    app.space(2)

    # TODO: Change this; text field should not display video_id; what if car name has "("? Use last bracket as input
    selected_video_id = re.search('\((.*?)\)', selection_wordcloud).group(1)
    df_feature_adj = _get_df_feature_adj(selected_video_id, feature)

    if len(df_feature_adj) < 1:
        st.write(
            "This feature is not mentioned. Please try using a different feature.")
    else:
        _generate_wordcloud(df_feature_adj)
