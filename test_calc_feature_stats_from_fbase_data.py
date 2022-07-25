# Calculate feature stats for video_id from sentiment_1 data in fb

from firebase_admin import credentials, firestore
import pandas as pd
import json
from pandas import json_normalize
from utils import fb
from utils import features

# Setup
fb.firebase_init()
db = firestore.client()
brand = "Tesla"
model = "Model 3"
video_id = "3YI7Lxop0n8"

# Get data, convert to dict, convert to df
sentiment_1 = fb.get_data(db, brand, model, video_id, field="sentiment_1")["sentiment_1"]
dict = json.loads(sentiment_1)
df = pd.DataFrame.from_dict(dict)
print(df.head())

# Calc feature stats
feature_list = features.get_defined_feature_list()
feature_df = features.get_features(df, feature_list)
feature_stats = features.get_feature_stats(feature_df, feature_list)
print(feature_stats)


print(fb.upload_df(feature_stats, "videoid", "filename"))
print("")
print("DOWNLAOD")
print("")
print(fb.download_df("videoid", "filename"))

# import toml
# from firebase_admin import credentials, initialize_app, storage


# # Put your local file path 
# bucket = storage.bucket()
# blob = bucket.blob("boom.csv")
# blob.upload_from_string(feature_stats.to_csv())

# # Opt : if you want to make public access from the URL
# blob.make_public()

# print("your file url", blob.public_url)
