from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import clean

#-----------------------------------------------------------------------

# Generate and save a wordcloud

def generate_wordcloud(dir, df, file_name="wordcloud"):
    all_words = " ".join([w for w in df["content_no_stopwords"]])
    wordcloud = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(all_words)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(dir + "/" + file_name + ".jpg")