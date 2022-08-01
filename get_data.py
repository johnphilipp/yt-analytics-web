from utils.video import Video
import pandas as pd

input = pd.read_csv("data/input.csv")
for i in range(len(input)):
    c = input.iloc[i].to_list()
    video = Video(c[0], c[1], c[2], str(c[3]), c[4])

    # 1) Meta
    print("\n1) Meta (" + video.get_video_id() + ")")
    meta = video.get_meta()
    video.post_meta_supabase(video.get_car_id(), meta)

    # 2) Content
    print("2) Content (" + video.get_video_id() + ")")
    content = video.get_content_raw()
    video.post_content_supabase(content)

    # 3) Sentiment
    print("\n3) Sentiment (" + video.get_video_id() + ")")
    sentiment = video.get_sentiment_transformers(content)
    video.post_sentiment_supabase(sentiment)
