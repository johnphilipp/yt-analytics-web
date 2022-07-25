import sys
import os
from pathlib import Path
import yt
import sb
import clean
import sentiment
import wcloud
import features

# -----------------------------------------------------------------------

main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, "../data")

# -----------------------------------------------------------------------


class Video:
    def __init__(self, make, model, trim, year, url):
        self._make = make
        self._model = model
        self._trim = trim
        self._year = year
        self._url = url
        self._video_id = self._parse_video_id(url)
        # Path(self._dir).mkdir(parents=True, exist_ok=True)

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

    def post_meta(self, db, meta):
        """
        Post meta data of self to Firebase.
        """
        return fb.post_meta(db, self._make, self._model, self._video_id, meta)

    def get_content_raw(self):
        """
        Return the content (comments and replies) of self via YouTube API.
        """
        return yt.get_content_raw(self._video_id)

    def post_content(self, db, content_json):
        return fb.post_content(db, self._make, self._model, self._video_id, content_json)

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

    def get_feature_stats(self, df, feature_list):
        """
        Return the feature stats of self.
        """
        df_features = features.get_features(df, feature_list)
        return features.get_feature_stats(df_features, feature_list)

    # def get_wordcloud(self):
    #     """
    #     Return the wordcloud of self.
    #     """
    #     df = pd.read_csv(self._dir + "/content_clean.csv", header=[0], lineterminator='\n')
    #     df = df.drop(['Unnamed: 0'], axis=1, errors='ignore')
    #     df_no_stopwords = clean.remove_stopwords(self._dir, df)
    #     wcloud.generate_wordcloud(self._dir, df_no_stopwords)

    def get_car_id(self):
        return sb.get_car_id(self._make, self._model, self._trim, self._year)

    def post_meta_supabase(self, car_id, meta):
        return sb.insert_meta(self._video_id, car_id, meta)

    def post_content_supabase(self, content):
        return sb.insert_content(self._video_id, content)

    def post_sentiment_supabase(self, sentiment):
        return sb.insert_sentiment(self._video_id, sentiment)

# -----------------------------------------------------------------------

# Testing


def main():
    input = [
        ["Make", "Model", "Trim", "Year", "Url"],
        ["Tesla", "Model S", "P100D", "2020",
            "https://www.youtube.com/watch?v=mHhZ9jk-DrU"],
        ["Polestar", "2", "Standard", "2021",
            "https://www.youtube.com/watch?v=gY9VVmbM2J8"],
        ["VW", "ID.4", "Standard", "2021",
            "https://www.youtube.com/watch?v=5rVSw9r7LQc"],
        ["Tesla", "Model 3", "Standard", "2019",
            "https://www.youtube.com/watch?v=kbulCM90w8w"],
        ["Tesla", "Model Y", "Standard", "2022",
            "https://www.youtube.com/watch?v=PZ8NPeYFPCY"]
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

    # -----------------------------------------------------------------------

    # # 4) Feature stats
    # # 4.1) Get feature stats
    # print("\n4) Feature stats (" + video.get_video_id() + ")")
    # print("4.1) Get feature stats")
    # feature_list = features.get_defined_feature_list()
    # key = "feature_stats"
    # feature_stats_df = video.get_feature_stats(sentiment_1_df, feature_list)
    # feature_stats_json = {key: feature_stats_df.to_dict()}
    # print(feature_stats_json[key])
    # # 4.2) Post feature stats
    # print("4.2) Post feature stats")
    # print(video.post_content(db, feature_stats_json))

    # #-----------------------------------------------------------------------

    # # 5) Generate wordcloud
    # print("")
    # print("3) Generate wordcloud")
    # video.get_wordcloud()


if __name__ == '__main__':
    main()
