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
brand = "Porsche"
model = "911 Turbo S"
video_id = "E8W6BEc2fZw"

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

