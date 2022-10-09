import sys
import os
from pathlib import Path
import utils.sb as sb
import utils.yt as yt
import utils.clean as clean
import utils.sentiment as sentiment


class Video:
    """
    Extract video data from YouTube, Transform, Load into Supabase
    """

    def __init__(self, make, model, trim, year, url):
        self._make = make
        self._model = model
        self._trim = trim
        self._year = year
        self._url = url
        self._video_id = self._parse_video_id(url)

    def _parse_video_id(self, url):
        """
        Get video id from video url
        """
        if "youtu.be" in url:  # e.g., https://youtu.be/kbulCM90w8w
            vid = url.rsplit('/', 1)[-1]
            if "?" in url:  # e.g., https://youtu.be/kbulCM90w8w?t=269
                vid = vid.split("?", 1)[0]
        elif "youtube.com" in url:  # e.g., https://www.youtube.com/watch?v=kbulCM90w8w
            vid = url.rsplit('v=', 1)[-1]
            if "&" in url:  # e.g., https://www.youtube.com/watch?v=kbulCM90w8w&t=3s
                vid = vid.split("&", 1)[0]
        else:
            print("URL invalid")
            sys.exit()
        return vid

    def get_url(self):
        """
        Return the url of self.
        """
        return self._url

    def get_video_id(self):
        """
        Return the video_id of self.
        """
        return self._video_id

    def content_exists(self):
        """
        Return True if content of self already exists.
        """
        file_path = os.path.join(self._dir, "content.csv")
        path = Path(file_path)
        return path.is_file()

    def get_meta(self):
        """
        Return meta data of self as dict via YouTube API.
        """
        return yt.get_meta(self._video_id)

    def get_content_raw(self):
        """
        Return the content (comments and replies) of self via YouTube API.
        """
        return yt.get_content_raw(self._video_id)

    def get_sentiment_transformers(self, df):
        """
        Return the sentiment of self via transformers.
        """
        df_basic_clean = clean.basic_clean(df)
        return sentiment.sentiment_transformers(df_basic_clean)

    def get_sentiment_textblob(self, df):
        """
        Return the sentiment of self via textblob.
        """
        df_basic_clean = clean.basic_clean(df)
        return sentiment.sentiment_textblob(df_basic_clean)

    def get_car_id(self):
        """
        Return car_id of a car from Supabase specified by Make, Model, Trim, Year.
        """
        return sb.get_car_id(self._make, self._model, self._trim, self._year)

    def post_meta_supabase(self, car_id, meta):
        """
        Post meta data to Supabase.
        """
        return sb.insert_meta(self._video_id, car_id, meta)

    def post_content_supabase(self, car_id, content):
        """
        Post content data to Supabase.
        """
        return sb.insert_content(self._video_id, car_id, content)

    def post_sentiment_supabase(self, car_id, sentiment):
        """
        Post sentiment data to Supabase.
        """
        return sb.insert_sentiment(self._video_id, car_id, sentiment)


def main():
    """
    Testing
    """
    input = [
        ["Make", "Model", "Trim", "Year", "Url"]
    ]

    for i in range(1, len(input)):
        # for i in range(2, 3):
        video = Video(input[i][0], input[i][1], input[i]
                      [2], input[i][3], input[i][4])

        # -----------------------------------------------------------------------

        # 1) Meta
        # 1.1) Get meta
        print("\n1) Meta (" + video.get_video_id() + ")")
        print("1.1) Get meta")
        meta = video.get_meta()
        # 1.2) Post meta
        print("1.2) Post meta")
        video.post_meta_supabase(video.get_car_id(), meta)

        # -----------------------------------------------------------------------

        # 2) Content
        # 2.1) Get content
        print("\n2) Content (" + video.get_video_id() + ")")
        print("2.1) Get content")
        content = video.get_content_raw()
        # 2.2) Post content
        # print("2.2) Post content")
        # print(video.post_content_supabase(content))

        # -----------------------------------------------------------------------

        # 3) Sentiment
        # 3.1) Get sentiment
        print("\n3) Sentiment (" + video.get_video_id() + ")")
        print("3.1) Get sentiment")
        sentiment = video.get_sentiment_transformers(content)
        # 3.2) Post sentiment
        print("3.2) Post sentiment")
        print(video.post_sentiment_supabase(sentiment))


if __name__ == '__main__':
    main()
