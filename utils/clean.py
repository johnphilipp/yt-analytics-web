from string import punctuation
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd

#-----------------------------------------------------------------------

# Return a df with cleaned content (remove @abc mentions, links, and 
# punctuation)

def basic_clean(dir, df):
    # Creating function to clean comments
    def clean(content):
        content = re.sub(r"@[A-Za-z0-9]+", "", content)
        content = re.sub(r"https?:\/\/\S+", "", content)
        content = re.sub(r"http?:\/\/\S+", "", content)
        content = content.translate(str.maketrans("", "", punctuation))
        return content

    # Cleaning content
    df["content_clean"] = df["content"].apply(clean)

    # Write df to csv
    df.to_csv(dir + "/content_clean.csv")  

    return df

#-----------------------------------------------------------------------

# Return a df where stopwords are removed from content

def remove_stopwords(dir, df):
    # Download and select stopwords
    nltk.download('stopwords')
    english_stop_words = stopwords.words('english')

    # Func which removes stopwords
    def stop_word_removal_nltk(x):
        token = x.split()
        return " ".join([w for w in token if not w in english_stop_words])

    # Remove col[0] (csv index) and NaNs
    df = df.drop(df.columns[0], axis=1)
    df = df[df["content_clean"].notnull()]

    # Remove stopwords and create new col in df
    df["content_no_stopwords"]  = df["content_clean"].apply(stop_word_removal_nltk)

    # Write df to csv
    df.to_csv(dir + "/content_no_stopwords.csv")  

    return df