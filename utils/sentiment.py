import clean
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
import pandas as pd
import os

#-----------------------------------------------------------------------

# Return a df with sentiment score based on transformers

def sentiment_transformers(df):
    # Initiate model
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    def sentiment_score(review):
        tokens = tokenizer.encode(review, return_tensors='pt')
        result = model(tokens)
        # result.logits # prints tensor
        return int(torch.argmax(result.logits))+1
    
    # Claculate sentiment
    df["sentiment"] = df["content_clean"].apply(lambda x: sentiment_score(x[:512]))

    return df

#-----------------------------------------------------------------------

# Return a df with sentiment score (subjectivity and polarity) based on 
# textblob

def sentiment_textblob(df):
    # Create func to get subjectivity
    def get_subjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # Create func to get polarity
    def get_polarity(text):
        return TextBlob(text).sentiment.polarity

    # Create two new cols
    df["subjectivity"] = df["content_clean"].apply(get_subjectivity)
    df["polarity"] = df["content_clean"].apply(get_polarity)

    # Create func to compute pos, neg, neutr
    def get_analysis(score):
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"

    # Create new col
    df["analysis"] = df["polarity"].apply(get_analysis)

    return df
