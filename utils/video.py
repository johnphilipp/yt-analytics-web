import os
from pathlib import Path
import pandas as pd
from utils import content
from utils import clean
from utils import sentiment
from utils import wcloud
from utils import features

#-----------------------------------------------------------------------

main_dir = os.path.dirname(__file__)
data_dir = os.path.join(main_dir, "../data")

#-----------------------------------------------------------------------

class Video: 
    def __init__(self, car, channel, url, features):
        self._car = car
        self._channel = channel
        self._url = url
        self._features = features
        self._dir = os.path.join(data_dir, car.replace(" ", "_"), channel.replace(" ", "_"))
        Path(self._dir).mkdir(parents=True, exist_ok=True)

    def get_car_name(self):
        """
        Return the car name of self.
        """
        return self._car
    
    def get_channel_name(self):
        """
        Return the channel name of self.
        """
        return self._channel

    def get_url(self):
        """
        Return the url of self.
        """
        return self._url

    def get_features(self):
        """
        Return the car name of self.
        """
        return self._features

    def get_dir(self):
        """
        Return the data dir of self.
        """
        return self._dir
    
    def content_exists(self):
        """
        Return True if content of self already exists.
        """
        file_path = os.path.join(self._dir, "content.csv")
        path = Path(file_path)
        return path.is_file()

    def get_content(self):
        """
        Return the content (comments and replies) of self via YouTube API.
        """
        content.get_content(self._dir, self._url)

    def get_sentiment(self):
        """
        Return the sentiment of self.
        """
        df = pd.read_csv(self._dir + "/content.csv", header=[0], lineterminator='\n')
        df = df.drop(['Unnamed: 0'], axis=1, errors='ignore')
        df_basic_clean = clean.basic_clean(self._dir, df)
        sentiment.sentiment_transformers(self._dir, df_basic_clean)
        sentiment.sentiment_textblob(self._dir, df_basic_clean)

    def get_wordcloud(self):
        """
        Return the wordcloud of self.
        """
        df = pd.read_csv(self._dir + "/content_clean.csv", header=[0], lineterminator='\n')
        df = df.drop(['Unnamed: 0'], axis=1, errors='ignore')
        df_no_stopwords = clean.remove_stopwords(self._dir, df)
        wcloud.generate_wordcloud(self._dir, df_no_stopwords)

    def get_feature_stats(self):
        """
        Return the feature stats of self.
        """
        df = pd.read_csv(self._dir + "/sentiment_1.csv", header=[0], lineterminator='\n')
        df = df.drop(['Unnamed: 0'], axis=1, errors='ignore')
        df_features = features.get_features(self._dir, df, self._features)
        features.get_feature_stats(self._dir, df_features, self._features)

#-----------------------------------------------------------------------

# Testing

def main():
    car = "Chevrolet Caprice Donk"
    channel = "TopGear"
    url = "https://www.youtube.com/watch?v=OKKyxnR_UM8"
    features = ["rim", "steering wheel", "engine", "color", "colour",
                "carbon", "light", "design", "sound", "interior", 
                "exterior", "mirror", "body", "brake", "chassis", 
                "suspension", "gearbox", "navigation", "infotainment"]

    video = Video(car, channel, url, features)

    #-----------------------------------------------------------------------

    # 0) Retrieve basic information
    print("")
    print("0) Retrieve basic information")
    car = video.get_car_name()
    dir = video.get_dir()
    print(car)
    print(video.get_channel_name())
    print(video.get_url())
    print(video.get_features)
    print(dir)

    #-----------------------------------------------------------------------

    # 1) Get content
    print("")
    print("1) Get content for " + video.get_car_name())
    video.get_content()

    #-----------------------------------------------------------------------

    # 2) Calculate sentiment
    print("")
    print("2) Calculate sentiment")
    video.get_sentiment()

    #-----------------------------------------------------------------------

    # 3) Generate wordcloud
    print("")
    print("3) Generate wordcloud")
    video.get_wordcloud()

    #-----------------------------------------------------------------------

    # 4) Get feature stats
    print("")
    print("4) Get feature stats")
    video.get_feature_stats()

if __name__ == '__main__':
    main()