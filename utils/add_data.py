from model.Video import Video
import pandas as pd
import streamlit as st


def get_meta(video):
    """
    Get meta data via YouTube API
    """
    st.spinner("1/6) Get meta data")
    return video.get_meta()


def get_content(video):
    """
    Get post and comment content via YouTube API
    """
    with st.spinner("2/6) Scrape content"):
        return video.get_content_raw()


def get_sentiment(video, content):
    """
    Get sentiment data calculated from content 
    via custom Transformers model
    """
    with st.spinner("3/6) Calculate sentiment"):
        return video.get_sentiment_transformers(content)


def post_meta(video, meta):
    """
    Post meta to Supabase
    """
    with st.spinner("4/6) Push meta data to database"):
        video.post_meta_supabase(video.get_car_id(), meta)


def post_content(video, content):
    """
    Post content to Supabase
    """
    with st.spinner("5/6) Push content to database"):
        video.post_content_supabase(video.get_car_id(), content)


def post_sentiment(video, sentiment):
    """
    Post sentiment to Supabase
    """
    with st.spinner("6/6) Push sentiment to database"):
        video.post_sentiment_supabase(video.get_car_id(), sentiment)


def run():
    input = pd.read_csv("data/input.csv")
    for i in range(6):  # len(input)
        c = input.iloc[i].to_list()
        video = Video(str(c[0]), str(c[1]), str(c[2]), str(c[3]), str(c[4]))
        print(c)

        print("\n1) Get Meta (" + video.get_video_id() + ")")
        meta = get_meta(video)
        print("2) Get Content (" + video.get_video_id() + ")")
        content = get_content(video)
        print("3) Get Sentiment (" + video.get_video_id() + ")")
        sentiment = get_sentiment(video, content)

        print("\n1) Post Meta (" + video.get_video_id() + ")")
        post_meta(video, meta)
        print("2) Post Content (" + video.get_video_id() + ")")
        post_content(video, content)
        print("3) PostSentiment (" + video.get_video_id() + ")")
        post_sentiment(video, sentiment)


if __name__ == "__main__":
    run()
