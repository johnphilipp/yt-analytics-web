from wordcloud import WordCloud
import clean
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------

# Generate and save a wordcloud


def generate_wordcloud(df):
    # from PIL import Image
    # image = Image.open('sunrise.jpg')
    # st.image(image, caption='Sunrise by the mountains')

    df = clean.basic_clean(df)
    df = clean.remove_stopwords(df)
    all_words = " ".join([w for w in df["content_no_stopwords"]])
    wordcloud = WordCloud(width=500, height=300, random_state=21,
                          max_font_size=119).generate(all_words)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return plt
    # plt.savefig("wordcloud.jpg")
