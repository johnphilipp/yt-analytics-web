from utils import clean
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import en_core_web_sm


def get_df_feature_adj(df_feature):
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


def get_wordcloud(df):
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
