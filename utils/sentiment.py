from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
import pandas as pd


def sentiment_transformers(df):
    """
    Return a df with sentiment score based on transformers
    """
    tokenizer = AutoTokenizer.from_pretrained(
        'nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained(
        'nlptown/bert-base-multilingual-uncased-sentiment')

    def sentiment_score(review):
        """
        Calculate sentiment score
        """
        tokens = tokenizer.encode(review, return_tensors='pt')
        result = model(tokens)
        # result.logits # prints tensor
        return int(torch.argmax(result.logits))+1

    df["sentiment_score"] = df["content_clean"].apply(
        lambda x: sentiment_score(x[:512]))

    return df


def sentiment_textblob(df):
    """
    Return a df with sentiment score (subjectivity and polarity) based on
    textblob
    """
    def get_subjectivity(text):
        """
        Return subjectivity
        """
        return TextBlob(text).sentiment.subjectivity

    def get_polarity(text):
        """
        Return polarity
        """
        return TextBlob(text).sentiment.polarity

    df["subjectivity"] = df["content_clean"].apply(get_subjectivity)
    df["polarity"] = df["content_clean"].apply(get_polarity)

    def get_analysis(score):
        """
        Return pos, neg, neutr sentiment label
        """
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"

    df["analysis"] = df["polarity"].apply(get_analysis)

    return df
