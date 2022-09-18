from string import punctuation
import re
import nltk
from nltk.corpus import stopwords
import streamlit as st


def basic_clean(df):
    """
    Return a df with cleaned content (remove @abc mentions, links, and
    punctuation)
    """
    def clean(content):
        content = re.sub(r"@[A-Za-z0-9]+", "", content)
        content = re.sub(r"https?:\/\/\S+", "", content)
        content = re.sub(r"http?:\/\/\S+", "", content)
        content = content.translate(str.maketrans("", "", punctuation))
        return content

    df["content_clean"] = df["content"].apply(clean)

    return df


def remove_stopwords(df):
    """
    Return a df where stopwords are removed from content
    """
    @st.cache(suppress_st_warning=True)
    def _download_nltk_stopwords():
        """
        Download nltk stopwords package
        """
        nltk.download("stopwords")

    _download_nltk_stopwords()
    english_stop_words = stopwords.words('english')

    def _edit_df(df):
        """
        Remove col[0] (csv index) and NaNs
        """
        df = df.drop(df.columns[0], axis=1)
        df = df[df["content_clean"].notnull()]
        return df

    df = _edit_df(df)

    def _remove_stop_words(x):
        """
        Remove stopwords
        """
        token = x.split()
        return " ".join([w for w in token if not w in english_stop_words])

    df["content_no_stopwords"] = df["content_clean"].apply(
        _remove_stop_words)

    return df
